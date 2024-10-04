"""This script pulls metadata from the API, transforms it, and then uploads it into S3."""

from transform_metadata import create_csvs
from load_metadata import load_into_s3


if __name__ == "__main__":

    create_csvs()
    load_into_s3()
