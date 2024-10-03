import asyncio
import aiohttp

BASE_URL = "https://data-eng-plants-api.herokuapp.com/plants/"


async def fetch_data(session, plant_id: int):

    response = await session.request("GET", BASE_URL+str(plant_id))

    return await response.json()


async def get_plant_data():

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, i) for i in range(1, 51)]

        responses = await asyncio.gather(*tasks)

        return responses


if __name__ == "__main__":

    print(asyncio.run(get_plant_data()))
