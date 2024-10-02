"""Given a file name uploads local json file to S3 bucket."""

from json import loads
from datetime import datetime

from database_handler import get_connection, get_botanist_ids, get_plant_ids


def read_json(file_path: str) -> dict:
    """Opens a json file and returns a dictionary."""
    with open(file_path, 'r', encoding='UTF-8') as f:
        content = f.read()
    return loads(content)


def convert_at_datetime(date_str: str) -> datetime:
    """Converts a date string in 'YYYY-MM-DD HH:MM:SS' format to a datetime object."""
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')


def convert_last_watered_datetime(date_str: str) -> datetime:
    """Converts a date string in RFC 1123 format to a datetime object."""
    return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')


def format_reading_tuples(data: dict) -> list[tuple]:
    """Formats the readings data for database insertion."""
    readings = []
    botanist_info = get_botanist_ids()

    for reading in data:
        plant_id = reading['plant_id']
        botanist_id = botanist_info[reading['botanist_name']]

        at = convert_at_datetime(reading['at'])
        soil_moisture = reading['soil_moisture']
        temperature = reading['temperature']
        last_watered = convert_last_watered_datetime(reading['last_watered'])

        readings.append((plant_id, botanist_id, at,
                        soil_moisture, temperature, last_watered))
    return readings


def upload_readings(file_path: str):
    """Uploads the reading/recording information to the database."""
    data = read_json(file_path)
    tuples = format_reading_tuples(data)
    plant_ids = get_plant_ids()
    filtered_tuples = [
        reading for reading in tuples if reading[0] in plant_ids]
    insert_query = """INSERT INTO beta.reading (plant_id, botanist_id, 
    at, soil_moisture, temperature, last_watered) VALUES """

    value_placeholders = []
    values = []

    for reading in filtered_tuples:
        value_placeholders.append("( %s, %s, %s, %s, %s, %s )")
        values.extend(reading)  # Flatten the reading tuple

        full_query = insert_query + ", ".join(value_placeholders) + ";"

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(full_query, values)
            conn.commit()
