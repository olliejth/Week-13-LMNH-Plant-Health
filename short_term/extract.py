"""Extract plant recording data"""

import multiprocessing
from datetime import datetime
import json

import requests as req

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_object_name() -> str:
    """Gets the name for the object, based on the current time."""

    current_time = datetime.now()
    object_name = datetime.strftime(current_time,
                                    "recording-%Y-%m-%d-%H-%M.json")
    return object_name


def chunk_data(data: list, num_chunks: int) -> list:
    """Splits data into a specified number of chunks."""
    chunk_size = len(data) // num_chunks + \
        (len(data) % num_chunks > 0)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def get_plant_data(plant_ids: list) -> list[dict]:
    """Makes the API calls for a given list of plant IDs and returns the raw JSON files."""
    # implement ASYNC here using grequests
    results = [req.get(BASE_URL + str(plant_id), timeout=10)
               for plant_id in plant_ids]
    return [res.json() for res in results]


def get_recording_info(reading_data: dict) -> dict:
    """Gets the relevant recording data from the reading."""

    if "error" in reading_data.keys():
        return None

    plant_id = reading_data["plant_id"]
    botanist_name = reading_data.get("botanist", {"name": None})["name"]
    at = reading_data["recording_taken"]
    soil_moisture = float(reading_data["soil_moisture"])
    temperature = float(reading_data["temperature"])
    last_watered = reading_data["last_watered"]

    return {
        "plant_id": plant_id,
        "botanist_name": botanist_name,
        "at": at,
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "last_watered": last_watered
    }


def extract_recordings() -> str:
    """Gets the recordings and turns them into json data.
    The main function to be called from the pipeline."""

    plant_ids = list(range(1, 50 + 1))
    num_chunks = multiprocessing.cpu_count()
    print(f"using {num_chunks} parallel threads")
    plant_id_chunks = chunk_data(plant_ids, num_chunks)

    with multiprocessing.Pool() as pool:
        results = pool.map(get_plant_data, plant_id_chunks)

    api_data = [item for sublist in results for item in sublist]

    plant_data = []
    for element in api_data:
        recording_info = get_recording_info(element)
        if recording_info is not None:
            plant_data.append(recording_info)

    object_name = get_object_name()
    with open(object_name, "w", encoding='UTF-8') as f:
        json.dump(plant_data, f, indent=6)

    return object_name


if __name__ == '__main__':
    extract_recordings()
