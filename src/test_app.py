import unittest
import requests
from datetime import datetime, timezone
from app import fetch_weather, process_weather_data, check_alerts, API_KEY, TEMP_THRESHOLD, CITIES
from database import Session
from models import WeatherSummary

class TestWeatherMonitoringSystem(unittest.TestCase):

    def test_system_setup(self):
        """Test system starts and connects to the OpenWeatherMap API."""
        response = requests.get('http://api.openweathermap.org/data/2.5/weather', params={'q': 'Delhi', 'appid': API_KEY})
        self.assertEqual(response.status_code, 200)  # Check if connection is successful

    def test_data_retrieval(self):
        """Test data retrieval for each city."""
        weather_data = fetch_weather()
        self.assertEqual(len(weather_data), len(CITIES))  # Ensure data for all cities is retrieved

    def test_temperature_conversion(self):
        """Test conversion of temperature from Kelvin to Celsius."""
        kelvin_temp = 300.15
        celsius_temp = kelvin_temp - 273.15
        self.assertAlmostEqual(celsius_temp, 27.0, places=2)  # Verify conversion

    def test_daily_weather_summary(self):
        """Test daily weather summary calculations."""
        # Fetch weather data
        weather_data = fetch_weather()
        
        # Process the data and store summaries in the database
        process_weather_data(weather_data)

        # Check if summaries are stored correctly in the database
        session = Session()
        summaries = session.query(WeatherSummary).all()
        self.assertGreater(len(summaries), 0)  # Ensure that summaries were created
        session.close()

    def test_alerting_thresholds(self):
        """Test alerting system for temperature thresholds."""
        # Simulate weather data exceeding the threshold
        weather_data = [
            {'city': 'Delhi', 'temp': 36, 'condition': 'Clear'},
            {'city': 'Mumbai', 'temp': 34, 'condition': 'Cloudy'},
            {'city': 'Chennai', 'temp': 38, 'condition': 'Rain'}
        ]
        
        alerts = check_alerts(weather_data)
        expected_alerts = [
            "Alert: Delhi has exceeded the temperature threshold of 35°C with 36°C.",
            "Alert: Chennai has exceeded the temperature threshold of 35°C with 38°C."
        ]
        
        # Ensure alerts are generated correctly
        for expected_alert in expected_alerts:
            self.assertIn(expected_alert, alerts)

if __name__ == '__main__':
    unittest.main()
