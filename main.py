# main.py
import time
from weather_api import fetch_weather_data
from data_processing import store_weather_data, calculate_daily_summary
from alert_system import check_alerts

CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
INTERVAL = 300  # 5 minutes

def main():
    while True:
        for city in CITIES:
            weather_data = fetch_weather_data(city)
            if weather_data:
                store_weather_data(weather_data)
                calculate_daily_summary(city)
                check_alerts()

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
