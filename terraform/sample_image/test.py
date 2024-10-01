import json
from os import environ as ENV
from datetime import datetime
import boto3
from dotenv import load_dotenv


def get_object_names_with_timestamps(client, bucket_name: str) -> list[dict]:
    """Returns a list of object names and their last modified timestamps for a specific bucket."""

    objects = client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in objects:
        return []

    return [{"FilePath": o["Key"], "LastModified": o["LastModified"].isoformat()} for o in objects["Contents"]]


def lambda_handler(event, context):
    """Main handler function for the Lambda."""
    # Load environment variables if needed (for local testing)

    load_dotenv()

    print(f"Started process: {datetime.now()}")
    bucket_client = boto3.client(service_name="s3")

    files = get_object_names_with_timestamps(
        bucket_client, ENV['INPUT_BUCKET_NAME'])

    print("Files found:")
    for file in files:
        print(f"{file['FilePath']} ({file['LastModified']})")

    print(f"Finished process: {datetime.now()}")

    return {
        'statusCode': 200,
        'body': json.dumps(files)
    }


if __name__ == '__main__':
    lambda_handler({}, {})
