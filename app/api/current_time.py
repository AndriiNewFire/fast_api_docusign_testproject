from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from api.utilities import CitySchema, cities_database

router = InferringRouter()


@cbv(router)
class CurrentTimeZone:
    """
    This part is designed to retrieve a datetime of the selected aria
    API should receive a JSON in format {'name': $name_of_the_city, 'timezone': $timezone}
    List of possible timezones are available via this link - http://worldtimeapi.org/timezones
    """

    @router.get("/cities")
    def get_all_city_schemas(self):
        """
        Method to get all stored data of city_schemas requests
        """
        return cities_database

    @router.post('/cities')
    def get_city_scheme_timezone_and_append_db(self, city: CitySchema):
        """
        Method to get a datetime and append the database with it
        :param city: {'name': $name_of_the_city, 'timezone': $timezone}
        :return: time zone and local time
        """
        result = city.request_time_zone()

        return result

    @router.get("/cities/{identifier}")
    def get_specific_city_scheme(self, identifier: int = 0):
        """
        :param identifier: unique value of city_scheme in db
        :return: a data stored under that identifier
        """
        try:
            city = cities_database[identifier-1]
        except IndexError:
            # Defaults city to London as this is Greenwich +0:00 time
            city = {
                    'name': 'No items in DB',
                    'datetime': 'Default value - Europe/London',
                    }
        return city
