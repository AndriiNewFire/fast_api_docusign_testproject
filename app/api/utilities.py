from pydantic import BaseModel

import requests

cities_database = []


class CitySchema(BaseModel):
    name: str
    timezone: str

    def request_time_zone(self):

        link = f"http://worldtimeapi.org/api/timezone/{self.timezone}"

        result = requests.get(link).json()

        # Receiving time
        time = result.get('datetime', 'Nothing found')

        # Appending our local DB(list) with values
        cities_database.append({'name': self.name,
                                'datetime': time,
                                })
