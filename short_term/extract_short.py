"""Extract plant recording data"""

from datetime import datetime
import json
import time

from async_api_call import get_plant_data


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_object_name() -> str:
    """Gets the name for the object, based on the current time."""

    current_time = datetime.now()
    object_name = datetime.strftime(current_time,
                                    "recording-%Y-%m-%d-%H-%M.json")
    return object_name


def chunk_data(data: list, num_chunks: int) -> list:
    """Splits data into a specified number of chunks."""
    if not data:
        return []

    chunk_size = len(data) // num_chunks + \
        (len(data) % num_chunks > 0)
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


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
    print(f"Calling API")
    start_time = time.time()
    api_data = get_plant_data(plant_ids)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Received API data in {duration:.2f} seconds")

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
