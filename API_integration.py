from multiprocessing import Value
import os
from random import choice
from traceback import print_tb
import requests
from dotenv import load_dotenv

load_dotenv()

#function to get weather_info
def get_weather(city_name: str):
    api_key = os.getenv("API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    try:
        #Making GET request
        response = requests.get(url)
        response.raise_for_status()
        
        #Parse Json response
        weather_data = response.json()
        
        #Extract key details
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        weather = weather_data["weather"][0]["main"]
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        #Display the data
        print(f"=== Weather in {city}, {country} ===")
        print(f"Condition: {weather} ({description})")
        print(f"Temperature: {temperature}°C (Feels like {feels_like}°C)")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
        
    except requests.exceptions.RequestException as e:
        print("Error: Failed to fetch data from API.")
        print(f"Details: {e}")
    except KeyError:
        print("Error: Unexpected response format from API.")

#function to get crypto
def get_crypto():
    pass

#Program to showcase API's
while True:
    print("\nWhich data would you like to display")
    print("1. Weather Info")
    print("2. Cryptocurrency prices")
    print("3. exit")

    try:
        choice = int(input("Pick a choice(1,2,3): ").strip())
    except ValueError:
        print("Please enter a number")
        continue
    if choice == 1:
        city_name = input("Please enter a city name: ")
        get_weather(city_name)
    elif choice == 3:
        get_crypto()
    elif choice == 3:
        print("exiting!!............")
        break
    else:
        print("Invalid choice")
