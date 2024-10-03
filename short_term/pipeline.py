"""Whole pipeline script for short-term storage."""

<<<<<<< HEAD
import asyncio

from extract import extract_recordings
from transform import transform_recordings
from load import upload_readings
=======
from extract_short import extract_recordings
from transform_short import transform_recordings
from load_short import upload_readings
>>>>>>> c5178a18f6190646b4a0cd6ed19d29809b2aeaed


def lambda_handler(event=None, context=None):  # pylint: disable=W0613
    """Extracts and uploads API data to DB."""
    file_name = asyncio.run(extract_recordings())
    transformed_data = transform_recordings(file_name)
    upload_readings(transformed_data)

    return {
        'statusCode': 200,
        'body': ""
    }
