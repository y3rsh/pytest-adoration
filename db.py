import sys
import os
from pprint import pprint
import boto3
from botocore.exceptions import ClientError
from session import Session


TABLE_NAME = "Sessions"
DYNAMO_ENDPOINT = os.environ.get("DYNAMO_ENDPOINT", "http://localhost:8000")
REGION = os.environ.get("REGION", "local")


def get_dynamodb_resource():
    return boto3.resource("dynamodb", endpoint_url=DYNAMO_ENDPOINT, region_name=REGION)


def get_dynamodb_client():
    return boto3.client("dynamodb", endpoint_url=DYNAMO_ENDPOINT, region_name=REGION)


def create_test_run_table(dynamodb=None):
    if not dynamodb:
        dynamodb = get_dynamodb_resource()

    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "sessionid", "KeyType": "HASH"},],  # noqaE231
        AttributeDefinitions=[
            {"AttributeName": "sessionid", "AttributeType": "S"},
        ],  # noqaE231
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    return table


def put_session(session: Session, dynamodb=None):
    if not dynamodb:
        dynamodb = get_dynamodb_resource()

    table = dynamodb.Table(TABLE_NAME)
    item = vars(session)
    print(item)
    return table.put_item(Item=item)


def delete_test_run_table(dynamodb=None):
    if not dynamodb:
        dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(TABLE_NAME)
    print(table.delete())


def query_sessions(dynamodb=None):
    if not dynamodb:
        dynamodb = get_dynamodb_resource()

    table = dynamodb.Table(TABLE_NAME)
    return table.scan()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "delete":
            delete_test_run_table()
            exit(0)
        elif sys.argv[1] == "scan":
            pprint(query_sessions())
            exit(0)
    dynamodb_client = get_dynamodb_client()
    table = None
    try:
        table = dynamodb_client.describe_table(TableName=TABLE_NAME)
    except ClientError as ce:
        if ce.response["Error"]["Code"] == "ResourceNotFoundException":
            print(f"table does not exist: {ce}")
    if table:
        print(f"table {table}")
    else:
        test_run_table = create_test_run_table()
        print("Table status:", test_run_table.table_status)
