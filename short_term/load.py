"""Given a file name uploads local json file to S3 bucket."""
from os import environ as ENV

from database_handler import get_connection


def upload_recordings(data: list[tuple]):
    """Uploads the reading/recording information to the database."""
    insert_query = """INSERT INTO reading(plant_id, botanist_id, 
    at, soil_moisture, temperature, last_watered)
    VALUES %s"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(insert_query, data)
        conn.commit()
