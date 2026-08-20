import requests


class WeatherService:

    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude, longitude, days_from_now=0):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_sum,"
                "wind_speed_10m_max,"
                "relative_humidity_2m_mean,"
                "cloud_cover_mean,"
                "weather_code"
            ),
            "timezone": "auto",
            "forecast_days": days_from_now + 1
        }

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            index = days_from_now

            return {
                "temperature_max": data["daily"]["temperature_2m_max"][index],
                "temperature_min": data["daily"]["temperature_2m_min"][index],
                "rain": data["daily"]["precipitation_sum"][index],
                "wind": data["daily"]["wind_speed_10m_max"][index],
                "humidity": data["daily"]["relative_humidity_2m_mean"][index],
                "clouds": data["daily"]["cloud_cover_mean"][index],
                "weather_code": data["daily"]["weather_code"][index]
            }
        except (requests.RequestException, KeyError, IndexError) as e:
            print(f"Error al obtener el clima en WeatherService: {e}")
            return None