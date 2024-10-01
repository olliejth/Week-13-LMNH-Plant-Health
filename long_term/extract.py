"""Extracts all of the json files from the S3 bucket more than 24h old."""

from os import environ as ENV
from datetime import datetime, timedelta
from dotenv import load_dotenv
from boto3 import client


def get_object_names(s3_client):
    """Returns the name of all relevant files."""

    objects = s3_client.list_objects(
        Bucket=ENV["BUCKET_NAME"])["Contents"]

    return [obj["Key"] for obj in objects
            if obj["Key"].startswith("recordings/recording")]


def is_more_than_a_day_old(bucket_object: str,
                           current_time: datetime) -> bool:
    """Is this objects more than a day old?"""

    object_date = datetime.strptime(bucket_object[21:],
                                    "%Y-%m-%d-%H-%M.json")
    time_diff = current_time - object_date

    return time_diff.days >= 1


def filter_old_objects(bucket_objects: list[str],
                       current_time: datetime = datetime.now()) -> list[str]:
    """Returns all of the objects more than 24 hours old."""

    return [bucket_object
            for bucket_object in bucket_objects
            if is_more_than_a_day_old(bucket_object, current_time)]


def download_most_recent_file():
    """Downloads the most recent file.
        The main function to be called from the pipeline code."""

    load_dotenv()

    s3 = client(service_name="s3",
                aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    file_names = get_object_names(s3)
    most_recent = get_latest_object_string(file_names)

    to_be_downloaded = ENV["OBJECT_NAME_PREFIX"]+most_recent

    s3.download_file(
        Bucket=ENV["INPUT_BUCKET_NAME"],
        Key=to_be_downloaded,
        Filename=most_recent
    )
    return most_recent


if __name__ == "__main__":

    load_dotenv()
    s3 = client(service_name="s3",
                aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])
    print(filter_old_objects(get_object_names(s3)))
