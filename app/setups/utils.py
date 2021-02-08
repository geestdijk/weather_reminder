from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string

from core.models import User, UserForecast
from core.serializers import UserForecastListSerializer


def send_email_with_weather_update(email):
    date = datetime.today().strftime("%d/%m/%Y")
    subject = f"Weather update for {date}"
    user = User.objects.get(email=email)
    user_weather_forecasts = UserForecast.objects.filter(user=user)
    forecasts = UserForecastListSerializer(user_weather_forecasts, many=True).data
    data = extract_weather_data(forecasts)
    html_content = render_to_string("setups/weather_update_email.html", data)
    return send_mail(subject,
                     html_content,
                     from_email=None,
                     recipient_list=[email, ],
                     html_message=html_content)


def extract_weather_data(forecasts):
    data = {'cities': {}}
    for city_forecast in forecasts:
        city_name = city_forecast['city']['name']
        data['cities'][city_name] = {}
        # 4-days forecast for the city
        daily_forecasts = city_forecast['city']['forecast']['daily'][0:4]
        for daily_forecast in daily_forecasts:
            date_string = datetime.fromtimestamp(daily_forecast['dt']).strftime("%d/%m/%Y")
            min_temp = round(daily_forecast['temp']['min'])
            max_temp = round(daily_forecast['temp']['max'])
            wind_speed = round(daily_forecast['wind_speed'], 1)
            data['cities'][city_name][date_string] = {
                'min_temp': min_temp,
                'max_temp': max_temp,
                'wind_speed': wind_speed
            }
    return data
