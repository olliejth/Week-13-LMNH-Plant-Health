import grequests
import requests
import time

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


def make_requests():  # this is alot faster
    async_list = []
    for i in range(1, 50):
        url = f"{BASE_URL}{i}"
        action_item = grequests.get(url)
        async_list.append(action_item)

    responses = grequests.map(async_list)

    for i, response in enumerate(responses, 1):
        print(f"Response {i}: {response.json()}")


def make_requests2():
    sync_list = []
    for i in range(1, 50):
        url = f"{BASE_URL}{i}"
        response = requests.get(url)
        sync_list.append(response)

    for i, response in enumerate(sync_list, 1):
        print(f"Response {i}: {response.json()}")


if __name__ == "__main__":
    start_time = time.time()
    print("Making asynchronous requests...")
    make_requests()
    async_duration = time.time() - start_time
    print(f"Asynchronous requests took: {async_duration:.2f} seconds\n")

    start_time = time.time()
    print("Making synchronous requests...")
    make_requests2()
    sync_duration = time.time() - start_time
    print(f"Synchronous requests took: {sync_duration:.2f} seconds")
