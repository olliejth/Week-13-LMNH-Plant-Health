"""Transforms the json data into csvs."""

import csv
from extract_metadata import extract_api_data


def turn_into_csv_input(data: list[dict]) -> list[list]:
    """Turns a list of dictionaries into the rows of a csv"""

    headings = data[0].keys()

    rows = []
    for item in data:
        rows.append([item[key] for key in headings])

    rows = [headings] + rows

    return rows


def create_csvs() -> None:
    """Creates the csv files for the metadata."""

    api_data = extract_api_data()

    botanist_data = [plant["botanist_data"] for plant in api_data]
    location_data = [plant["location_data"] for plant in api_data]
    plant_data = [plant["plant_data"] for plant in api_data]

    with open("botanists.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerows(turn_into_csv_input(botanist_data))
    with open("locations.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerows(turn_into_csv_input(location_data))
    with open("plants.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerows(turn_into_csv_input(plant_data))
