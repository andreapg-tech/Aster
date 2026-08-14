import requests


class LocationService:

    def __init__(self):
        self.base_url = "https://geocoding-api.open-meteo.com/v1/search"

    def get_coordinates(self, location):

        params = {
            "name": location,
            "count": 1,
            "language": "es",
            "format": "json"
        }

        response = requests.get(
            self.base_url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if "results" not in data:
            return None

        result = data["results"][0]

        return {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "name": result["name"],
            "country": result.get("country")
        }