from fastapi import APIRouter
from pydantic import BaseModel

import requests

"""

"""
current_time_router = APIRouter()
cities_database = []


class City(BaseModel):
    name: str
    timezone: str


async def request_time_zone(city):
    result = requests.get(f"http://worldtimeapi.org/api/timezone/{city['timezone']}").json()
    return result


@current_time_router.get("/cities")
def get_all_cities():
    return cities_database


@current_time_router.post('/cities')
def append_city(city: City):
    cities_database.append(city.dict())
    return cities_database[-1]


@current_time_router.get("/cities/{identifier}")
async def get_specific_city(identifier: int = 0):
    final_result = {}

    try:
        city = cities_database[identifier-1]
    except IndexError:
        # Defaults city to London as this is Greenwich +0:00 time
        city = {
                'name': 'No items in DB, default value for Europe/London',
                'timezone': 'Europe/London',
                }
    result = await request_time_zone(city)

    final_result[city['name']] = result.get('datetime', 'No datetime found')

    return final_result
