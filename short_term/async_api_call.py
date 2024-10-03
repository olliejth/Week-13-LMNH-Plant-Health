"""This scripts sends all of the calls to the API efficiently using grequests."""

import grequests


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data(plant_ids: list[int]):
    """Sends simultaneous calls to the API."""

    async_list = []
    for i in plant_ids:
        url = f"{BASE_URL}{i}"
        action_item = grequests.get(url)
        async_list.append(action_item)

    responses = grequests.map(async_list)

    return [response.json() if response is not None
            else {"error": True}
            for response in responses]
