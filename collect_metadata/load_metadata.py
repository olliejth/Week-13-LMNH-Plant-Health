"""Upload the metadata to the S3 bucket."""

from os import environ as ENV

from dotenv import load_dotenv
from boto3 import client

load_dotenv()


def load_into_s3() -> None:
    """Loads the csv files to the S3 bucket."""

    file_names = ["botanists.csv",
                  "locations.csv",
                  "plants.csv"]

    s3 = client(service_name="s3",
                aws_access_key_id=ENV["AWS_rvbyaulf_KEY"],
                aws_secret_access_key=ENV["AWS_rvbyaulf_SECRET_KEY"])

    for file_name in file_names:

        s3.upload_file(file_name, ENV["BUCKET_NAME"], f"metadata/{file_name}")
