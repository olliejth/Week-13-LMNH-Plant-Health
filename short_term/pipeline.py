"""Whole pipeline script for short-term storage."""

from extract import extract_recordings
from transform import transform_recordings
from load import upload_readings


def lambda_handler(event=None, context=None):  # pylint: disable=W0613
    """Extracts and uploads API data to DB."""
    file_name = extract_recordings()
    transformed_data = transform_recordings(file_name)
    upload_readings(transformed_data)

    return {
        'statusCode': 200,
        'body': ""
    }
