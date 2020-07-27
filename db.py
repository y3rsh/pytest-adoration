import sys
import os
from pprint import pprint
import boto3
import logging
from botocore.exceptions import ClientError
from botocore.exceptions import EndpointConnectionError
from botocore.client import Config
from session import Session

logger = logging.getLogger(__name__)

TABLE_NAME = "Sessions"
DYNAMO_LOCAL_URL = os.environ.get("DYNAMO_LOCAL_URL", "http://localhost:8000")


def no_connection(func):
    def wrapper(*args):
        if not args[0].db_connection:
            return None
        else:
            return func(*args)

    return wrapper


class DynamoSessions:
    def __init__(self, local=True):
        self.local = local
        self.config = Config(connect_timeout=3, retries={"max_attempts": 0})
        self.db_connection = True
        self.dynamo_resource = self.get_dynamodb_resource()
        self.dynamo_client = self.get_dynamodb_client()

    def get_dynamodb_resource(self):
        if self.local:
            return boto3.resource(
                "dynamodb",
                endpoint_url=DYNAMO_LOCAL_URL,
                region_name="local",
                config=self.config,
            )
        else:
            return boto3.resource("dynamodb", config=self.config)

    def get_dynamodb_client(self):
        if self.local:
            return boto3.client(
                "dynamodb",
                endpoint_url=DYNAMO_LOCAL_URL,
                region_name="local",
                config=self.config,
            )
        else:
            return boto3.client("dynamodb", config=self.config)

    @no_connection
    def create_sessions_table(self):
        try:
            table = self.dynamo_resource.create_table(
                TableName=TABLE_NAME,
                KeySchema=[
                    {"AttributeName": "sessionid", "KeyType": "HASH"},
                ],  # noqaE231
                AttributeDefinitions=[
                    {"AttributeName": "sessionid", "AttributeType": "S"},
                ],  # noqaE231
                ProvisionedThroughput={
                    "ReadCapacityUnits": 10,
                    "WriteCapacityUnits": 10,
                },
            )
            return table
        except EndpointConnectionError as e:
            logger.warning(f"Not connected to dynamo {e}")
            self.db_connection = False

    @no_connection
    def put_session(self, session: Session):
        try:
            table = self.dynamo_resource.Table(TABLE_NAME)
            item = vars(session)
            print(item)
            return table.put_item(Item=item)
        except EndpointConnectionError as e:
            logger.warning(f"Not connected to dynamo {e}")
            self.db_connection = False

    @no_connection
    def delete_test_run_table(self):
        try:
            table = self.dynamo_resource.Table(TABLE_NAME)
            logger.info(table.delete())
        except EndpointConnectionError as e:
            logger.warning(f"Not connected to dynamo {e}")
            self.db_connection = False

    @no_connection
    def query_sessions(self):
        try:
            table = self.dynamo_resource.Table(TABLE_NAME)
            return table.scan()
        except EndpointConnectionError as e:
            logger.warning(f"Not connected to dynamo {e}")
            self.db_connection = False


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.INFO,
    )
    db = DynamoSessions()
    if len(sys.argv) == 2:
        if sys.argv[1] == "delete":
            db.delete_test_run_table()
            exit(0)
        elif sys.argv[1] == "scan":
            logger.info(pprint(db.query_sessions()))
            exit(0)
    table = None
    try:
        table = db.get_dynamodb_client().describe_table(TableName=TABLE_NAME)
    except ClientError as ce:
        if ce.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.info(f"table does not exist: {ce}")
    if table:
        print(f"table {table}")
    else:
        test_run_table = db.create_sessions_table()
        logger.info(f"Table status after create: {test_run_table.table_status}")
