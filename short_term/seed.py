"""Script to seed the database with initial metadata values."""

from os import environ as ENV

import pandas as pd

from dotenv import load_dotenv
import boto3

from database_handler import get_connection


def download_metadata():
    """Downloads the botanists, plants, and locations metadata from the
    S3 bucket for seeding."""
    load_dotenv()
    s3 = boto3.client('s3')
    metadata_path = 'metadata/'
    file_names = ['botanists.csv', 'locations.csv', 'plants.csv']
    for file_name in file_names:
        s3_file_path = f"{metadata_path}{file_name}"
        local_file_path = f"./{file_name}"
        s3.download_file(ENV['BUCKET_NAME'], s3_file_path, local_file_path)


def upload_locations():
    """Uploads the locations metadata to the database."""
    locations_df = pd.read_csv('locations.csv')
    locations_df = locations_df.dropna()
    locations_tuple = [(row['latitude'], row['longitude'], row['town'],
                        row['timezone']) for _, row in locations_df.iterrows()]

    with get_connection() as conn:
        cursor = conn.cursor()
        insert_query = """INSERT INTO beta.origin_location
        (latitude, longitude, town, timezone)
        VALUES (%s, %s, %s, %s)"""
        cursor.executemany(insert_query, locations_tuple)
        conn.commit()


def upload_plants():
    """Uploads the plants data into the database."""
    plants_df = pd.read_csv('plants.csv')
    plants_df = plants_df.dropna()
    locations = get_locations()
    tuples = [format_plant_tuple(row, locations)
              for _, row in plants_df.iterrows()]

    with get_connection() as conn:
        cursor = conn.cursor()
        insert_query = """INSERT INTO beta.plant
        (plant_id, plant_name, plant_scientific_name, origin_location_id,
        small_url, medium_url, original_url, regular_url, thumbnail_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(insert_query, tuples)
        conn.commit()


def format_plant_tuple(row: dict, location_dict: dict) -> tuple:
    """Formats a plant dictionary row for database insertion."""
    location_id = location_dict.get(row['location_name'])
    return (row['plant_id'], row['plant_name'], row['plant_scientific_name'], location_id,
            row['small_url'], row['medium_url'], row['regular_url'],
            row['original_url'], row['thumbnail_url'])


def get_locations() -> dict:
    """Returns a dictionary mapping town name to location id."""
    query = "SELECT location_id, town FROM beta.origin_location;"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return {x['town']: x['location_id'] for x in results}


if __name__ == "__main__":
    # download_metadata()
    upload_locations()
    upload_plants()
