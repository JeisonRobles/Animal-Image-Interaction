import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE")

def _session():
    if AWS_PROFILE:
        return boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    return boto3.Session(region_name=AWS_REGION)

def s3_client():
    return _session().client("s3")

def ddb_table():
    table_name = os.getenv("DDB_TABLE", "AnimalImages")
    return _session().resource("dynamodb").Table(table_name)