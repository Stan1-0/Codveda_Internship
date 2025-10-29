import requests
import os

city_name = input("Please enter a city name: ")

api_key = os.environ['API_KEY']

url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"


try:
    #Making GET request
    response = requests.get(url)
    response.raise_for_status()
    
    #Parse Json response
    weather_data = response.json()
except requests.exceptions.RequestException as e:
    print("Error: Failed to fetch data from API.")
    print(f"Details: {e}")
except KeyError:
    print("Error: Unexpected response format from API.")
