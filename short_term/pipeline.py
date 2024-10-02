"""Whole pipeline script for short-term storage."""

from short_term.extract_short import extract_recordings
from short_term.transform_short import transform_recordings
from short_term.load_short import upload_readings


def lambda_handler(event=None, context=None):
    """Extracts and uploads API data to DB."""
    file_name = extract_recordings()
    transformed_data = transform_recordings(file_name)
    upload_readings(transformed_data)

    return {
        'statusCode': 200,
        'body': ""
    }
