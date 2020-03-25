import requests
import credentials
import re

cities = ["Thane,in"]
weather_dict = {}

def city_forecast(city):
  response = requests.get(
          "https://community-open-weather-map.p.rapidapi.com/forecast?q="+city,
          headers={
          "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
          "X-RapidAPI-Key": credentials.rapidapi_key
        },
  )

  return response.json()


weather_dict[cities[0]] = city_forecast(cities[0])

temperature = int(int(weather_dict[cities[0]]['list'][0]['main']['temp'])-273.15)
sky = weather_dict[cities[0]]['list'][0]['weather'][0]['main']
# print(temperature)
# print(sky)
# print(weather_dict)