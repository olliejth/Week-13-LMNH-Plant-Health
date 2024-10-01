"""Whole pipeline script for short-term storage."""

from extract import extract_recordings
from load import load_recordings


def lambda_handler(event=None, context=None):
    """Extracts and uploads API data to S3."""

    file_name = extract_recordings()
    load_recordings(file_name)

    return {
        'statusCode': 200,
        'body': ""
    }
