markdown
Copy code
# Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates

## Overview
This project implements a real-time data processing system for monitoring weather conditions in major Indian cities. It fetches real-time weather data from the OpenWeatherMap API, processes it, and provides insights on temperature, humidity, wind speed, and dominant weather conditions. The system also includes alerting features based on user-configurable temperature thresholds and visualizations of weather trends.

## Features
- Fetches weather data for multiple cities.
- Processes and summarizes daily weather data.
- Sends alerts when temperature thresholds are exceeded.
- Provides weather forecasts.
- Visualizes temperature trends and dominant weather conditions.

## Technologies Used
- Python 3.10
- Flask (for the API)
- SQLAlchemy (for database management)
- OpenWeatherMap API
- Matplotlib (for data visualization)
- Docker (for containerization)
  
## Prerequisites
- Python 3.10 or higher
- Docker (if you want to run the application in a container)

## Clone the Repository
To clone this repository, run the following commands in your terminal:

```bash
git clone https://github.com/Sonikashankar/Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates.git
cd Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates

## Install Dependencies
If you choose to run the application outside of Docker, install the required Python packages using the following command:

```bash
pip install -r src/requirements.txt



## Install Dependencies
- If you choose to run the application outside of Docker, install the required Python packages:

```bash
pip install -r src/requirements.txt

## Configure Environment Variables
-Create a .env file in the src directory and add your OpenWeatherMap API key:

```env
Copy code
OPENWEATHER_API_KEY=65034db418bdca607af12535618e19c9
## Note: Ensure that you replace the example API key with your own key when deploying the application.

## Running the Application
A. Running Locally
Set Up Environment Variables: Ensure your .env file is properly configured with your API key.

Run the Application: Execute the following command in the src directory:

```bash
Copy code
python src/app.py
This will start the application, fetching and processing weather data at the defined intervals.

B. Running with Docker
Build the Docker Container: To build the Docker image, run the following command in the root directory of the project:

```bash
Copy code
docker build -t weather_monitoring .
Run the Docker Container: To run the Docker container, use the following command, ensuring to set your OpenWeatherMap API key as an environment variable:

```bash
Copy code
docker run -d --env OPENWEATHER_API_KEY=65034db418bdca607af12535618e19c9 weather_monitoring
## Application Structure
src/app.py: The main application file responsible for fetching, processing, and storing weather data.
src/database.py: Handles database sessions and connections.
src/models.py: Contains the data models used to interact with the database.
src/requirements.txt: Lists all required Python packages for the application.
src/visualization.py: (If applicable) Handles data visualization for the processed weather data.
## Design Choices
Modular Architecture: The application is divided into separate modules for fetching data, processing it, and handling database interactions, promoting maintainability and readability.
Database Storage: SQLAlchemy is used for efficient database management, enabling seamless data manipulation and retrieval.
Alert Mechanism: The application checks for temperature thresholds and generates alerts when necessary, enhancing user awareness of weather conditions.
Alerts
The application monitors the temperature for each city and generates alerts if the temperature exceeds the defined threshold (default: 35°C). Alerts will be logged to the console for easy monitoring.







