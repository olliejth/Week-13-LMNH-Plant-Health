"""This script is for getting plant metadata from the API, and storing it in the S3 bucket."""

import requests as req

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data() -> list[dict]:
    """Makes the API calls and returns the raw json files."""

    results = [req.get(BASE_URL+str(i))
               for i in range(1, 5)]

    return [res.json() for res in results]


def get_botanist_data(raw_botanist_data: dict) -> dict:
    """Returns the relevant metadata of the botanist."""

    name = raw_botanist_data["name"].split(" ")

    return {
        "first_name": name[0],
        "last_name": name[-1],
        "email": raw_botanist_data["email"],
        "phone": raw_botanist_data["phone"]
    }


def get_location_data(raw_location_data: dict) -> dict:
    """Returns the relevant metadata of the location."""


def extract_relevant_data(reading_data: dict) -> dict:
    """Gets only the relevant metadata from a plant's data."""


if __name__ == "__main__":

    print(get_plant_data())
