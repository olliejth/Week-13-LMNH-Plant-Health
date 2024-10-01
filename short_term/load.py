"""Given a file name uploads local json file to S3 bucket."""

from boto3 import client


def get_s3_client(env: dict):
    """Returns boto3 s3 client."""
    return client(service_name="s3",
                  aws_access_key_id=env["AWS_ACCESS_KEY"],
                  aws_secret_access_key=env["AWS_SECRET_ACCESS_KEY"])


def upload_csv(filename, s3_client, env) -> None:
    """Uploads json file by name to S3 bucket."""
    bucket = env["BUCKET_NAME"]
    upload_filename = f"recordings/{filename}"

    s3_client.upload_file(filename, bucket, upload_filename)


def load_recordings(env: dict, file_name: str) -> None:
    """Calls extract and load scripts."""
    s3 = get_s3_client(env)

    upload_csv(file_name, s3, env)
