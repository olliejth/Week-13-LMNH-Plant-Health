"""Extract plant recording data"""

from datetime import datetime
import json
import requests as req

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data(number: int = 50) -> list[dict]:
    """Makes the API calls and returns the raw json files."""

    results = [req.get(BASE_URL+str(i))
               for i in range(1, number + 1)]

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


if __name__ == "__main__":

    api_data = get_plant_data(10)

    plant_data = [get_recording_info(element)
                  for element in api_data]

    print(plant_data)

    with open("recordings.json", "w") as f:
        json.dump(plant_data, f, indent=6)
