# src/visualization.py

import requests
import matplotlib.pyplot as plt
from datetime import datetime, timezone

API_KEY = '65034db418bdca607af12535618e19c9'  # Use the same API key
API_URL = 'http://api.openweathermap.org/data/2.5/weather'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def fetch_weather():
    weather_data = []
    for city in CITIES:
        response = requests.get(API_URL, params={'q': city, 'appid': API_KEY})
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            weather = data['weather'][0]
            wind = data['wind']

            weather_data.append({
                'city': city,
                'temp': main['temp'] - 273.15,  # Convert from Kelvin to Celsius
                'humidity': main['humidity'],
                'wind_speed': wind['speed'],
                'condition': weather['main'],
                'timestamp': data['dt']
            })
    return weather_data

def plot_weather_data():
    weather_data = fetch_weather()
    cities = [entry['city'] for entry in weather_data]
    temps = [entry['temp'] for entry in weather_data]
    humidities = [entry['humidity'] for entry in weather_data]
    wind_speeds = [entry['wind_speed'] for entry in weather_data]

    plt.figure(figsize=(12, 6))

    # Temperature Plot
    plt.subplot(3, 1, 1)
    bars = plt.bar(cities, temps, color='orange')
    plt.title('Current Temperature in Cities')
    plt.xlabel('City')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid()

    # Annotate temperature values
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}', ha='center', va='bottom')

    # Humidity Plot
    plt.subplot(3, 1, 2)
    bars = plt.bar(cities, humidities, color='blue')
    plt.title('Current Humidity in Cities')
    plt.xlabel('City')
    plt.ylabel('Humidity (%)')
    plt.xticks(rotation=45)
    plt.grid()

    # Annotate humidity values
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}', ha='center', va='bottom')

    # Wind Speed Plot
    plt.subplot(3, 1, 3)
    bars = plt.bar(cities, wind_speeds, color='green')
    plt.title('Current Wind Speed in Cities')
    plt.xlabel('City')
    plt.ylabel('Wind Speed (m/s)')
    plt.xticks(rotation=45)
    plt.grid()

    # Annotate wind speed values
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    plot_weather_data()
