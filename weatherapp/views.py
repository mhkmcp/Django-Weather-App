import requests
from django.shortcuts import render
from . models import City
from . forms import CityForm


def index(request):
    my_api_key = 'your-api-key'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.all()

    weather_data = []
    for city in cities:
        req = requests.get(url.format(city, my_api_key)).json()
        city_weather = {
            'city': city.name,
            'temperature': req['main']['temp'],
            'description': req['weather'][0]['description'],
            'icon': req['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weatherapp/index.html', context=context)
