"""This script is for getting plant metadata from the API, and storing it in the S3 bucket."""

from datetime import datetime
from zoneinfo import ZoneInfo
import requests as req

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data(number: int = 50) -> list[dict]:
    """Makes the API calls and returns the raw json files."""

    results = [req.get(BASE_URL+str(i))
               for i in range(1, number + 1)]

    return [res.json() for res in results]


def extract_botanist_data(raw_botanist_data: dict) -> dict:
    """Returns the relevant metadata of the botanist."""

    if raw_botanist_data.get("name"):
        name = raw_botanist_data.get("name").split(" ")
    else:
        name = (None, None)

    return {
        "first_name": name[0],
        "last_name": name[-1],
        "email": raw_botanist_data.get("email"),
        "phone": raw_botanist_data.get("phone")
    }


def get_timezone_from_region(region: str) -> str:
    """Returns the timezone from a region."""

    dt = datetime(2024, 9, 9, 12, 00, tzinfo=ZoneInfo(region))

    return dt.tzname()


def extract_location_data(raw_location_data: list | None) -> dict:
    """Returns the relevant metadata of the location."""

    if raw_location_data is None:
        latitude = None
        longitude = None
        town = None
        timezone = None
    else:
        latitude = float(raw_location_data[0])
        longitude = float(raw_location_data[1])
        town = raw_location_data[2]
        timezone = get_timezone_from_region(raw_location_data[-1])

    return {
        "latitude": latitude,
        "longitude": longitude,
        "town": town,
        "timezone": timezone
    }


def extract_plant_data(reading_data: dict) -> dict:
    """Returns the relevant metadata of the plant."""

    image_data = reading_data.get("images", {})
    plant_data = {
        "plant_id": reading_data.get("plant_id"),
        "plant_name": reading_data.get("name"),
        "plant_scientific_name": reading_data.get("scientific_name", [None])[0],
        "small_url": image_data.get("small_url"),
        "medium_url": image_data.get("medium_url"),
        "regular_url": image_data.get("regular_url"),
        "original_url": image_data.get("original_url"),
        "thumbnail_url": image_data.get("thumbnail")
    }

    return plant_data


def extract_relevant_data(reading_data: dict) -> dict:
    """Gets only the relevant metadata from a plant's data."""

    botanist_data = extract_botanist_data(reading_data.get("botanist", {}))
    location_data = extract_location_data(
        reading_data.get("origin_location"))
    plant_data = extract_plant_data(reading_data)

    return {
        "botanist_data": botanist_data,
        "location_data": location_data,
        "plant_data": plant_data
    }


def extract_api_data() -> list[dict]:
    """Extracts data from the API.
        This is the main function that should be called from the outside."""

    plants = get_plant_data(50)

    plant_data = []
    for i in range(0, len(plants)):
        plant_data.append(extract_relevant_data(plants[i]))

    return plant_data
