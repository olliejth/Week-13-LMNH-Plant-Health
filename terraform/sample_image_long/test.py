"""Sample script to run on lambda while ETL pipelines are developed"""
import json
from os import environ as ENV
from datetime import datetime

from boto3 import client
from dotenv import load_dotenv


def get_object_names_with_timestamps(client, bucket_name: str) -> list[dict]:
    """Returns a list of object names and their last modified timestamps for a specific bucket."""

    objects = client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in objects:
        return []

    return [{"FilePath": o["Key"],
             "LastModified": o["LastModified"].isoformat()}
            for o in objects["Contents"]]


def lambda_handler(event, context):  # pylint: disable=W0613
    """Main handler function for the Lambda."""

    print(f"Started process: {datetime.now()}")
    bucket_client = client(service_name="s3",
                           aws_access_key_id=ENV["AWS_rvbyaulf_KEY"],
                           aws_secret_access_key=ENV["AWS_rvbyaulf_SECRET_KEY"])

    files = get_object_names_with_timestamps(
        bucket_client, ENV['BUCKET_NAME'])

    print("Files found:")
    for file in files:
        print(f"{file['FilePath']} ({file['LastModified']})")

    print(f"Finished process: {datetime.now()}")

    return {
        'statusCode': 200,
        'body': json.dumps(files)
    }


if __name__ == '__main__':
    load_dotenv()
    lambda_handler({}, {})
