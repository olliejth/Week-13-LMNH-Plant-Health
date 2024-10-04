"""Whole pipeline script for short-term storage."""

from extract_short import extract_recordings
from transform_short import transform_recordings
from load_short import upload_readings


def lambda_handler(event=None, context=None):  # pylint: disable=W0613
    """Extracts and uploads API data to DB."""
    plant_data = extract_recordings()
    transformed_data = transform_recordings(plant_data)
    upload_readings(transformed_data)

    return {
        'statusCode': 200,
        'body': ""
    }
