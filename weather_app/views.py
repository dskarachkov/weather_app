from django.shortcuts import render
import requests
import datetime
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="MyApp")


def index(request):
    current_weather_url = 'https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m&hourly=temperature_2m,'

    if request.method == 'POST':
        city = request.POST['city'].title()

        weather_data, daily_forecasts = fetch_weather_and_forecast(city, current_weather_url)

        context = {
            'weather_data': weather_data,
            'daily_forecasts': daily_forecasts,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, current_weather_url):
    location = geolocator.geocode(city)
    # При ошибке получения координат города функция возвращает None
    try:
        lat, lon = location.latitude, location.longitude
    except AttributeError:
        return None, None
    response = requests.get(current_weather_url.format(lat, lon)).json()

    weather_data = {
        'city': city,
        'temperature': response['current']['temperature_2m'],
        'lat': lat,
        'lon': lon,
    }

    time = response['hourly']['time']
    temp = response['hourly']['temperature_2m']

    daily_forecasts = []
    for i in range(7):
        daily_forecasts.append({
            'day': time[i*24][5:10].replace('-', '.'),
            'min_temp': min(temp[i*24:(i+1)*24-1]),
            'max_temp': max(temp[i*24:(i+1)*24-1]),
        })

    return weather_data, daily_forecasts
