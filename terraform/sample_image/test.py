"""Script to execute extract and transform pipeline"""

from os import path, remove, environ as ENV
from datetime import datetime

from boto3 import client
from dotenv import load_dotenv


def get_object_names_with_timestamps(client, bucket_name: str) -> list[dict]:
    """Returns a list of object names and their last modified timestamps for a specific bucket."""

    objects = client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in objects:
        return []

    return [{"FilePath": o["Key"], "LastModified": o["LastModified"]} for o in objects["Contents"]]


if __name__ == '__main__':
    load_dotenv()

    print(f"Starting process")
    bucket_client = client(service_name="s3",
                           aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                           aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    files = get_object_names_with_timestamps(
        bucket_client, ENV['INPUT_BUCKET_NAME'])

    print("Files found:")

    for file in files:
        print(f"{file["FilePath"]} ({file["LastModified"]})")

    print(f"Finished process")
