"""Script to load the JSON data and transform it, preparing for database insertion."""

from database_handler import get_botanist_ids


def format_tuple(data: dict, botanist_details) -> tuple:
    """Turns a dictionary of reading data into a formatted tuple.
    Replaces the botanist name with botanist ID."""
    botanist_id = botanist_details[data['botanist_name']]
    return (data['plant_id'], botanist_id, data['at'], data['soil_moisture'],
            data['temperature'], data['last_watered'])


def transform_recordings(plant_data: list[dict]) -> list[tuple]:
    """Reads list plant data and returns a list of tuples
    ready for database insertion."""

    botanist_details = get_botanist_ids()
    tuples = [format_tuple(row, botanist_details) for row in plant_data]
    return tuples
