import argparse
import requests
import os
import time

API_KEY = "dcfcf241b3974e2eb2083231230409"
API_URL = 'https://api.weatherapi.com/v1/current.json'

CITIES_FILE = 'favorite_cities.txt'

parser = argparse.ArgumentParser(description="Weather Checker")

parser.add_argument('--city', help="Specify the city for weather information")
parser.add_argument('--favorite', choices=['add', 'list', 'remove'], help="Manage favorite cities")
parser.add_argument('--auto-refresh', action='store_true', help="Enable auto-refresh")

cities = []

if os.path.isfile(CITIES_FILE):
    with open(CITIES_FILE, 'r') as file:
        cities = file.read().splitlines()

args = parser.parse_args()

def save_cities():
    with open(CITIES_FILE, 'w') as file:
        file.write('\n'.join(cities))

def get_weather(city):
    
    params = {
        'key': API_KEY,
        'q': city,
    }

    
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None


if args.city:
    weather_data = get_weather(args.city)
    if weather_data:
        current = weather_data.get('current', {})
        temp = current.get('temp_c')
        desc = current.get('condition', {}).get('text')
        if temp is not None and desc:
            print(f"Weather in {args.city}:")
            print(f"Temperature: {temp}°C")
            print(f"Description: {desc}")
        else:
            print(f"Weather data for {args.city} is not available.")
    else:
        print(f"Failed to retrieve weather data for {args.city}.")


if args.favorite:
    if args.favorite == 'add' and args.city:
        cities.append(args.city)
        save_cities()
        print(f"Added {args.city} to your list of favorite cities.")
    elif args.favorite == 'list':
        print("Listing favorite cities:")
        if not cities:
            print("No favorite cities added.")
        else:
            for city in cities:
                print(city)
    elif args.favorite == 'remove' and args.city:
        if args.city in cities:
            cities.remove(args.city)
            save_cities()
            print(f"Removed {args.city} from your list of favorite cities.")
        else:
            print(f"{args.city} is not in your list of favorite cities.")


if args.auto_refresh:
    while True:
        if cities:
            for city in cities:
                print("Auto-refreshing cities...")
                weather_data = get_weather(city)
                if weather_data:
                    current = weather_data.get('current', {})
                    temp = current.get('temp_c')
                    desc = current.get('condition', {}).get('text')
                    if temp is not None and desc:
                        print(f"Weather in {city}:")
                        print(f"Temperature: {temp}°C")
                        print(f"Description: {desc}")
                    else:
                        print(f"Weather data for {city} is not available.")
                else:
                    print(f"Failed to retrieve weather data for {city}.")
                time.sleep(20) 
            print("Auto-refreshing done.")
            break 
        else:
            print("No favorite cities to auto-refresh.")
            break  
