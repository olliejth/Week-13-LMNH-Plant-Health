"""Creates altair visualisations using pandas dataframes."""

from os import environ as ENV

from boto3 import client
from dotenv import load_dotenv

load_dotenv()


def get_s3_client():
    """Returns boto3 s3 client."""

    return client(service_name="s3",
                  aws_access_key_id=ENV["AWS_rvbyaulf_KEY"],
                  aws_secret_access_key=ENV["AWS_rvbyaulf_SECRET_KEY"])


def get_bucket_by_name(s3_client):
    """Returns a bucket given a specific name."""

    output_bucket = s3_client.list_objects(Bucket=ENV["BUCKET_NAME"])
    return output_bucket


def is_valid_file(file_name: str) -> bool:
    """Filters the bucket files by naming convention and filetype."""

    if file_name.startswith("recordings/") and file_name.endswith(".csv"):
        return True
    return False


def download_truck_data_files(s3_client, target_bucket) -> list[str]:
    """Downloads relevant files from S3."""

    file_names = []
    i = 0
    for file in target_bucket["Contents"]:
        if is_valid_file(file["Key"]):
            new_file_name = f"data_file_{i}.csv"
            file_names.append(new_file_name)
            s3_client.download_file(
                ENV["BUCKET_NAME"], file["Key"], new_file_name)
            i += 1

    return file_names


def extract_s3_files() -> list[str]:
    """"""

    s3 = get_s3_client()

    bucket = get_bucket_by_name(s3)

    files_downloaded = download_truck_data_files(s3, bucket)

    return files_downloaded


if __name__ == "__main__":

    extract_s3_files()
