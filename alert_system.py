# alert_system.py
import sqlite3

# Define threshold (e.g., temperature > 35°C)
THRESHOLD_TEMP = 35

def check_alerts():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Fetch the latest weather data
    cursor.execute('''
        SELECT city, temp, timestamp FROM weather_data
        ORDER BY timestamp DESC LIMIT 1
    ''')

    latest_weather = cursor.fetchone()
    if latest_weather:
        city, temp, timestamp = latest_weather

        if temp > THRESHOLD_TEMP:
            trigger_alert(city, temp, timestamp)

    conn.close()

def trigger_alert(city, temp, timestamp):
    print(f"ALERT: Temperature in {city} exceeded {THRESHOLD_TEMP}°C! (Current temp: {temp}°C at {timestamp})")

if __name__ == "__main__":
    check_alerts()
