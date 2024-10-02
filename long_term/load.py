"""Given a file name uploads local json file to S3 bucket."""
from os import environ as ENV
from datetime import date

from dotenv import load_dotenv
from boto3 import client
import pandas as pd


load_dotenv()


def create_csv(df: pd.DataFrame) -> str:
    """Creates local csv from pandas dataframe."""
    filename = f"summary-{date.today()}.csv"
    df.to_csv(filename, index=False)

    return filename


def get_s3_client():
    """Returns boto3 s3 client."""
    return client(service_name="s3",
                  aws_access_key_id=ENV["AWS_rvbyaulf_KEY"],
                  aws_secret_access_key=ENV["AWS_rvbyaulf_SECRET_KEY"])


def upload_csv(filename, s3_client) -> None:
    """Uploads csv file by name to S3 bucket."""
    bucket = ENV["BUCKET_NAME"]
    upload_filename = f"recordings/{filename}"

    s3_client.upload_file(filename, bucket, upload_filename)


def load_recordings(df: pd.DataFrame) -> None:
    """Uploads local csv file to S3 bucket"""

    file_name = create_csv(df)

    s3 = get_s3_client()

    upload_csv(file_name, s3)
