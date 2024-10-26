# data_processing.py
import sqlite3
from datetime import datetime, timedelta

def store_weather_data(data):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO weather_data (city, timestamp, main_condition, temp, feels_like)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['city'], data['timestamp'], data['main'], data['temp'], data['feels_like']))

    conn.commit()
    conn.close()

def calculate_daily_summary(city):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    today = datetime.now().date()
    start_of_day = datetime.combine(today, datetime.min.time()).timestamp()
    end_of_day = datetime.combine(today, datetime.max.time()).timestamp()

    cursor.execute('''
        SELECT temp, main_condition
        FROM weather_data
        WHERE city = ? AND timestamp BETWEEN ? AND ?
    ''', (city, start_of_day, end_of_day))

    data = cursor.fetchall()

    if data:
        temps = [row[0] for row in data]
        conditions = [row[1] for row in data]

        avg_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        min_temp = min(temps)
        dominant_condition = max(set(conditions), key=conditions.count)

        cursor.execute('''
            INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (city, today, avg_temp, max_temp, min_temp, dominant_condition))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Example: After storing data, process it for a city
    calculate_daily_summary('Delhi')
