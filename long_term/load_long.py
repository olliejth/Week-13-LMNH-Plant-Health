"""Given a file name uploads local json file to S3 bucket."""
from os import environ as ENV
from datetime import date

from dotenv import load_dotenv
from boto3 import client
import pandas as pd


load_dotenv()


def create_csv(df: pd.DataFrame) -> str:
    """Creates local csv from pandas dataframe."""

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Invalid data, input data must be a pandas dataframe.")

    filename = f"summary-{date.today()}.csv"
    df.to_csv(filename, index=False)

    return filename


def get_s3_client():
    """Returns boto3 s3 client."""

    return client(service_name="s3",
                  aws_access_key_id=ENV["AWS_rvbyaulf_KEY"],
                  aws_secret_access_key=ENV["AWS_rvbyaulf_SECRET_KEY"])


def get_ses_clent():
    """Returns boto3 ses client."""

    return client(service_name="ses", region_name='eu-west-2',
                  aws_access_key_id=ENV["AWS_rvbyaulf_KEY"],
                  aws_secret_access_key=ENV["AWS_rvbyaulf_SECRET_KEY"])


def send_email(ses_client, to_email: str, from_email: str, df: pd.DataFrame):
    """Sends an HTML email to the recipient with the DataFrame content."""
    html_table = df.to_html(index=False)

    html_body = f"""
    <html>
    <body>
        <h2>Archived Plant Readings</h2>
        <p>Successfully uploaded the following .csv summary to the S3 bucket:</p>
        {html_table}
    </body>
    </html>
    """
    ses_client.send_email(
        Source=from_email,
        Destination={
            'ToAddresses': [to_email]
        },
        Message={
            'Subject': {
                'Data': "Archived Plant Readings to S3"
            },
            'Body': {
                'Html': {
                    'Data': html_body
                }
            }
        }
    )


def upload_csv(filename, s3_client) -> None:
    """Uploads json file by name to S3 bucket."""

    bucket = ENV["BUCKET_NAME"]
    upload_filename = f"recordings/{filename}"

    s3_client.upload_file(filename, bucket, upload_filename)


def load_recordings(df: pd.DataFrame) -> None:
    """Uploads local csv file to S3 bucket"""

    file_name = create_csv(df)

    s3 = get_s3_client()
    ses = get_ses_clent()

    upload_csv(file_name, s3)
    send_email(ses, ENV['EMAIL_RECIPIENT'], ENV['EMAIL_SENDER'], df)
