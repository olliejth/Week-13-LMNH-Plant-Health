import asyncio
import requests as req


BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


async def fetch_data(plant_id: int):
    response = req.get(BASE_URL+str(plant_id))
    return await response.json()


async def make_requests():

    tasks = [fetch_data(i) for i in range(1, 11)]

    responses = await asyncio.gather(*tasks)

    for i, response in enumerate(responses, 1):
        print(f"Response {i}: {response}")


if __name__ == "__main__":
    asyncio.run(make_requests())
