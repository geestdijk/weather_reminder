import os, sys

import django


current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir + '/../..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_reminder.settings')
django.setup()


from core.models import City
from django.conf import settings
import requests


OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/onecall"
payload = {
    'units': 'metric',
    'exclude': 'hourly,minutely',
    'appid': settings.OPENWEATHERMAP_API_KEY
}


def update_cities_weather_forecats_from_api():
    for city in City.objects.all():
        payload['lat'], payload['lon'] = city.lat, city.long
        res = requests.get(OPENWEATHERMAP_URL, params=payload)
        city.forecast = res.json()
        city.save()


if __name__ == '__main__':
    update_cities_weather_forecats_from_api()
