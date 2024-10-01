"""Given a file name uploads local json file to S3 bucket."""
from os import environ as ENV
from dotenv import load_dotenv
from boto3 import client


load_dotenv()


def get_s3_client():
    """Returns boto3 s3 client."""
    return client(service_name="s3",
                  aws_access_key_id=ENV["AWS_KEY"],
                  aws_secret_access_key=ENV["AWS_SECRET_KEY"])


def upload_csv(filename, s3_client) -> None:
    """Uploads json file by name to S3 bucket."""
    bucket = ENV["BUCKET_NAME"]
    upload_filename = f"recordings/{filename}"

    s3_client.upload_file(filename, bucket, upload_filename)


def load_recordings(file_name: str) -> None:
    """Calls extract and load scripts."""

    s3 = get_s3_client()

    upload_csv(file_name, s3)
