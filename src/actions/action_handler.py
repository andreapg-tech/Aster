from datetime import datetime
from config.settings import DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_LOCATION
from services.weather_service import WeatherService
from services.location_service import LocationService


class ActionHandler:

    def __init__(self):
        self.weather_service = WeatherService()
        self.location_service = LocationService()

    def execute(self, intent):

        if intent.name == "get_current_time":
            return self.get_current_time()

        if intent.name == "get_current_date":
            return self.get_current_date()

        if intent.name == "get_weather":
            return self.get_weather(intent.parameters)

        return None

    def get_current_time(self):
        now = datetime.now()
        return now.strftime("%H:%M")

    def get_current_date(self):
        now = datetime.now()
        return now.strftime("%d/%m/%Y")

    def get_weather(self, parameters):

        days_from_now = parameters.get("days_from_now", 0)
        location = parameters.get("location")
        information = parameters.get("information", "general")

        latitude = DEFAULT_LATITUDE
        longitude = DEFAULT_LONGITUDE
        location_name = DEFAULT_LOCATION

        if location:
            coordinates = self.location_service.get_coordinates(location)

            if coordinates is None:
                return f"No he encontrado la ubicación {location}."

            latitude = coordinates["latitude"]
            longitude = coordinates["longitude"]
            location_name = coordinates["name"]

        data = self.weather_service.get_weather(
            latitude,
            longitude,
            days_from_now
        )

        if information == "temperature":
            return (
                f"En {location_name}, la temperatura máxima será de "
                f"{data['temperature_max']} grados y la mínima de "
                f"{data['temperature_min']}."
            )

        if information == "rain":
            return (
                f"En {location_name}, se esperan "
                f"{data['rain']} mm de precipitación."
            )

        if information == "wind":
            return (
                f"En {location_name}, la velocidad máxima del viento será de "
                f"{data['wind']} km/h."
            )

        if information == "humidity":
            return (
                f"En {location_name}, la humedad media será del "
                f"{data['humidity']}%."
            )

        if information == "clouds":
            return (
                f"En {location_name}, la nubosidad media será del "
                f"{data['clouds']}%."
            )

        return (
            f"En {location_name}, la temperatura máxima será de "
            f"{data['temperature_max']} grados, la mínima de "
            f"{data['temperature_min']} y se esperan "
            f"{data['rain']} mm de precipitación."
        )