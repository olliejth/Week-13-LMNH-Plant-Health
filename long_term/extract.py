"""Extracts all of the json files from the S3 bucket more than 24h old."""

import os
from os import environ as ENV
from datetime import datetime
import json
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


def download_old_files():
    """Downloads files more than 24hrs old.
        The main function to be called from the pipeline code."""

    load_dotenv()
    s3 = client(service_name="s3",
                aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    file_names = filter_old_objects(get_object_names(s3))

    recordings = []
    for file_name in file_names:

        s3.download_file(Bucket=ENV["BUCKET_NAME"],
                         Key=file_name,
                         Filename=file_name)

        s3.delete_object(Bucket=ENV["BUCKET_NAME"],
                         Key=file_name)

        with open(file_name, "r") as f:
            recordings.extend(json.load(f))

        os.remove(file_name)

    return recordings
