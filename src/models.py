# src/models.py

from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WeatherSummary(Base):
    __tablename__ = 'weather_summaries'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    avg_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)
    min_temp = Column(Float, nullable=False)
    dominant_condition = Column(String, nullable=False)
    avg_humidity = Column(Float)  # New column for humidity
    avg_wind_speed = Column(Float)  # New column for wind speed
