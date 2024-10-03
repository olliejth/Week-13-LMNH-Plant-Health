"""Script to load the JSON data and transform it, preparing for database insertion."""

from json import loads

from database_handler import get_botanist_ids


def format_tuple(data: dict, botanist_details) -> tuple:
    """Turns a dictionary of reading data into a formatted tuple.
    Replaces the botanist name with botanist ID."""
    botanist_id = botanist_details[data['botanist_name']]
    return (data['plant_id'], botanist_id, data['at'], data['soil_moisture'],
            data['temperature'], data['last_watered'])


def transform_recordings(file_name: str) -> list[tuple]:
    """Reads the recordings JSON file and returns a list of tuples
    ready for database insertion."""
    with open(file_name, 'r', encoding='UTF-8') as file:
        file_content = file.read()
        recording_dict = loads(file_content)
    botanist_details = get_botanist_ids()
    tuples = [format_tuple(row, botanist_details) for row in recording_dict]
    return tuples
