"""Whole pipeline script for short-term storage."""

import asyncio

from extract import extract_recordings
from transform import transform_recordings
from load import upload_readings


def lambda_handler(event=None, context=None):
    """Extracts and uploads API data to DB."""
    file_name = asyncio.run(extract_recordings())
    transformed_data = transform_recordings(file_name)
    upload_readings(transformed_data)

    return {
        'statusCode': 200,
        'body': ""
    }
