import sys
import os
from pprint import pprint
import boto3
import logging
from botocore.exceptions import ClientError
from botocore.exceptions import EndpointConnectionError
from botocore.client import Config
from session import Session
from stage import Stage

logger = logging.getLogger(__name__)

SESSIONS_TABLE_NAME = "Sessions"
STAGES_TABLE_NAME = "Stages"
DYNAMO_LOCAL_URL = os.environ.get("DYNAMO_LOCAL_URL", "http://localhost:8000")


def no_connection(func):
    def wrapper(*args):
        if not args[0].db_connection:
            return None
        else:
            return func(*args)

    return wrapper


class Dynamo:
    def __init__(self, local=True):
        self.local = local
        self.config = Config(connect_timeout=3, retries={"max_attempts": 1})
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
                TableName=SESSIONS_TABLE_NAME,
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
    def create_stages_table(self):
        try:
            table = self.dynamo_resource.create_table(
                TableName=STAGES_TABLE_NAME,
                KeySchema=[
                    {"AttributeName": "stageid", "KeyType": "HASH"},
                ],  # noqaE231
                AttributeDefinitions=[
                    {"AttributeName": "stageid", "AttributeType": "S"},
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
    def put_object(self, table_name, object):
        try:
            table = self.dynamo_resource.Table(table_name)
            item = vars(object)
            logger.debug(f"Item to be put in {table_name} = {item}")
            return table.put_item(Item=item)
        except EndpointConnectionError as e:
            logger.warning(f"Not connected to dynamo {e}")
            self.db_connection = False

    def put_session(self, session: Session):
        self.put_object(SESSIONS_TABLE_NAME, session)

    def put_stage(self, stage: Stage):
        self.put_object(STAGES_TABLE_NAME, stage)

    @no_connection
    def delete_table(self, table_name):
        try:
            table = self.dynamo_resource.Table(table_name)
            logger.info(table.delete())
        except EndpointConnectionError as e:
            logger.warning(f"Not connected to dynamo {e}")
            self.db_connection = False

    @no_connection
    def scan_table(self, table_name):
        try:
            table = self.dynamo_resource.Table(table_name)
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
    db = Dynamo()
    if len(sys.argv) == 2:
        if sys.argv[1] == "delete":
            db.delete_table(SESSIONS_TABLE_NAME)
            db.delete_table(STAGES_TABLE_NAME)
            exit(0)
        elif sys.argv[1] == "scan":
            logger.info(pprint(db.scan_table(SESSIONS_TABLE_NAME)))
            logger.info(pprint(db.scan_table(STAGES_TABLE_NAME)))
            exit(0)
    sessions = None
    try:
        sessions = db.get_dynamodb_client().describe_table(
            TableName=SESSIONS_TABLE_NAME
        )
        stages = db.get_dynamodb_client().describe_table(TableName=STAGES_TABLE_NAME)
    except ClientError as ce:
        if ce.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.info(f"table does not exist: {ce}")
    if sessions and stages:
        logger.info(f"table {sessions}")
        logger.info(f"table {stages}")
    else:
        sessions_table = db.create_sessions_table()
        logger.info(
            f"Sessions table status after create: {sessions_table.table_status}"
        )
        stages_table = db.create_stages_table()
        logger.info(f"Stages table status after create: {stages_table.table_status}")
