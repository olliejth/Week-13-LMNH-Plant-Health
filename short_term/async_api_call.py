"""This scripts sends all of the calls to the API efficiently using grequests."""

import json
import grequests


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"
TIMEOUT = 45


def handle_response(response):
    """Handles the response from the API call."""

    if response is not None:
        try:
            if response.status_code == 200:
                return response.json()

            return {
                "error": True,
                "status_code": response.status_code,
                "response": response.text
            }
        except json.JSONDecodeError:
            return {
                "error": True,
                "message": "Invalid JSON response",
                "response": response.text
            }
        except Exception as e:  # pylint: disable=W0718
            return {
                "error": True,
                "message": str(e),
                "response": response.text
            }
    else:
        return {"error": True, "message": "No response received"}


def get_plant_data(plant_ids: list[int]):
    """Sends simultaneous calls to the API."""

    async_list = []
    for i in plant_ids:
        url = f"{BASE_URL}{i}"
        action_item = grequests.get(url, timeout=TIMEOUT)
        async_list.append(action_item)

    responses = grequests.map(async_list)

    results = []
    for response in responses:
        result = handle_response(response)
        results.append(result)

    return results


if __name__ == '__main__':
    api_results = get_plant_data(list(range(1, 51)))

    print(len(api_results))
    print(len([x for x in api_results if "error" not in x]))
