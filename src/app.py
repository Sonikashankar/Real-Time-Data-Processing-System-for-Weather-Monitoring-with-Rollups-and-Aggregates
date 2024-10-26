# src/app.py

import requests
from datetime import datetime, timezone
from database import Session
from models import WeatherSummary
import time


API_KEY = '65034db418bdca607af12535618e19c9'  # Replace with your OpenWeatherMap API key
API_URL = 'http://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
FETCH_INTERVAL = 300  # Fetch every 5 minutes
TEMP_THRESHOLD = 35  # User-configurable temperature threshold
THRESHOLD_CONSECUTIVE_UPDATES = 2


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
                'feels_like': main['feels_like'] - 273.15,
                'humidity': main['humidity'],    # New parameter
                'wind_speed': wind['speed'],      # New parameter
                'condition': weather['main'],
                'timestamp': data['dt']
            })
    print(f"Final weather data: {weather_data}")
    return weather_data

def process_weather_data(weather_data):
    daily_summary = {}
    for entry in weather_data:
        date = datetime.fromtimestamp(entry['timestamp'], timezone.utc).date()
        temp = entry['temp']
        humidity = entry['humidity']
        wind_speed = entry['wind_speed']
        condition = entry['condition']

        if date not in daily_summary:
            daily_summary[date] = {
                'total_temp': 0,
                'count': 0,
                'max_temp': float('-inf'),
                'min_temp': float('inf'),
                'total_humidity': 0,
                'total_wind_speed': 0,
                'conditions': {}
            }

        daily_summary[date]['total_temp'] += temp
        daily_summary[date]['count'] += 1
        daily_summary[date]['max_temp'] = max(daily_summary[date]['max_temp'], temp)
        daily_summary[date]['min_temp'] = min(daily_summary[date]['min_temp'], temp)
        daily_summary[date]['total_humidity'] += humidity
        daily_summary[date]['total_wind_speed'] += wind_speed
        daily_summary[date]['conditions'][condition] = daily_summary[date]['conditions'].get(condition, 0) + 1

    # Save summaries to the database
    session = Session()
    for date, data in daily_summary.items():
        avg_temp = data['total_temp'] / data['count']
        avg_humidity = data['total_humidity'] / data['count']
        avg_wind_speed = data['total_wind_speed'] / data['count']
        dominant_condition = max(data['conditions'], key=data['conditions'].get)
        
        summary = WeatherSummary(
            date=date, 
            avg_temp=avg_temp, 
            max_temp=data['max_temp'], 
            min_temp=data['min_temp'], 
            dominant_condition=dominant_condition,
            avg_humidity=avg_humidity,
            avg_wind_speed=avg_wind_speed
        )
        session.add(summary)
    session.commit()
    session.close()

def check_alerts(weather_data):
    alerts = []
    for entry in weather_data:
        if entry['temp'] > TEMP_THRESHOLD:
            alerts.append(f"Alert: {entry['city']} has exceeded the temperature threshold of {TEMP_THRESHOLD}°C with {entry['temp']}°C.")
    return alerts

def fetch_forecast(city):
    response = requests.get(FORECAST_URL, params={'q': city, 'appid': API_KEY})
    if response.status_code == 200:
        return response.json()['list']
    return None

def summarize_forecast(forecast_data):
    summary = {}
    for entry in forecast_data:
        #date = datetime.utcfromtimestamp(entry['dt']).date()
        date = datetime.fromtimestamp(entry['dt'], tz=timezone.utc).date()
        main = entry['main']
        weather = entry['weather'][0]

        if date not in summary:
            summary[date] = {
                'total_temp': 0,
                'count': 0,
                'conditions': {}
            }

        temp = main['temp'] - 273.15  # Convert from Kelvin to Celsius
        summary[date]['total_temp'] += temp
        summary[date]['count'] += 1
        summary[date]['conditions'][weather['main']] = summary[date]['conditions'].get(weather['main'], 0) + 1

    for date, data in summary.items():
        avg_temp = data['total_temp'] / data['count']
        dominant_condition = max(data['conditions'], key=data['conditions'].get)
        summary[date] = {
            'avg_temp': avg_temp,
            'dominant_condition': dominant_condition
        }
    
    return summary

if __name__ == '__main__':
 
    consecutive_alerts = {city: 0 for city in CITIES}  # Initialize with zero alerts for each city

    while True:
        weather_data = fetch_weather()
        process_weather_data(weather_data)

        # Process alerts
        alerts = check_alerts(weather_data)
        for alert in alerts:
            print(alert)
            for entry in weather_data:
                if entry['temp'] > TEMP_THRESHOLD:
                    consecutive_alerts[entry['city']] += 1
                    if consecutive_alerts[entry['city']] >= THRESHOLD_CONSECUTIVE_UPDATES:
                        print(f"Final Alert: {entry['city']} has exceeded the temperature threshold for {THRESHOLD_CONSECUTIVE_UPDATES} consecutive updates.")
                else:
                    consecutive_alerts[entry['city']] = 0

        process_weather_data(weather_data)


        # Fetch and summarize forecast for each city
        for city in CITIES:
            forecast_data = fetch_forecast(city)
            if forecast_data:
                forecast_summary = summarize_forecast(forecast_data)
                print(f"Forecast summary for {city}: {forecast_summary}")

        # Wait for the next fetch interval
        time.sleep(FETCH_INTERVAL)
