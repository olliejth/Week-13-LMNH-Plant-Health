import grequests


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def get_plant_data(plant_ids: list[int]):
    async_list = []
    for i in plant_ids:
        url = f"{BASE_URL}{i}"
        action_item = grequests.get(url)
        async_list.append(action_item)

    responses = grequests.map(async_list)

    return [response.json() if response is not None else {"error": 'error'}
            for response in responses]
