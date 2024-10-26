# weather_monitor_backend.py

from flask import Flask, request, jsonify, render_template
import requests
import sqlite3
import threading
from collections import Counter
import time
from datetime import datetime, timedelta


app = Flask(__name__)

# SQLite Database setup
def init_db():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    temperature REAL,
                    feels_like REAL,
                    main_condition TEXT,
                    timestamp TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS daily_summary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    city TEXT,
                    avg_temp REAL,
                    max_temp REAL,
                    min_temp REAL,
                    dominant_condition TEXT)''')
    conn.commit()
    conn.close()

init_db()

API_KEY = 'API_KEY'  # Replace with your API key
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
SCHEDULE_INTERVAL = 300  # in seconds (5 minutes)

# Fetch weather data from OpenWeatherMap API
def fetch_weather_data(city):
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    weather_data = []
    if response.status_code == 200:
        data = response.json()
        # print(data)
        temp_celsius = round(data['main']['temp'] - 273.15, 2)
        feels_like_celsius = round(data['main']['feels_like'] - 273.15, 2)
        main_condition = data['weather'][0]['main']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute("INSERT INTO weather_data (city, temperature, feels_like, main_condition, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (city, temp_celsius, feels_like_celsius, main_condition, timestamp))

        weather_data = [{
            'temperature': data['main']['temp'],
            'main_condition': data['weather'][0]['main']
        }]
    conn.commit()
    conn.close()
    return weather_data
def fetch_temperature_data(city, period):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    
    if period == 'hourly':
        # Fetch hourly data for the past 24 hours from weather_data
        last_24_hours = datetime.now() - timedelta(hours=24)
        cursor.execute('''
            SELECT strftime('%H:%M', timestamp) AS hour, temperature 
            FROM weather_data
            WHERE city = ? AND timestamp >= ?
            ORDER BY timestamp ASC
        ''', (city, last_24_hours))
        data = cursor.fetchall()
        
    elif period == 'daily':
        # Fetch daily data from daily_summaries table (last 7 days)
        cursor.execute('''
            SELECT date, avg_temp 
            FROM daily_summary
            WHERE city = ?
            ORDER BY date DESC LIMIT 7
        ''', (city,))
        data = cursor.fetchall()
        
    elif period == 'weekly':
        # Aggregate data by week from daily_summaries table
        cursor.execute('''
            SELECT strftime('%Y-%W', date) AS week, AVG(avg_temp) 
            FROM daily_summary
            WHERE city = ?
            GROUP BY week
            ORDER BY week DESC LIMIT 4
        ''', (city,))
        data = cursor.fetchall()
        
    elif period == 'monthly':
        # Aggregate data by month from daily_summaries table
        cursor.execute('''
            SELECT strftime('%Y-%m', date) AS month, AVG(avg_temp) 
            FROM daily_summary
            WHERE city = ?
            GROUP BY month
            ORDER BY month DESC LIMIT 6
        ''', (city,))
        data = cursor.fetchall()
        
    else:
        data = []

    conn.close()

    # Format data for JSON response
    labels = [row[0] for row in data]
    temperatures = [row[1] for row in data]
    return {"labels": labels, "temperatures": temperatures}

# Schedule the weather data fetching
def schedule_weather_data():
    while True:
        for city in CITIES:
            weather_data = fetch_weather_data(city)
            if weather_data != None and weather_data != []:
                store_daily_summary(city, weather_data)
        time.sleep(SCHEDULE_INTERVAL)

def store_daily_summary(city, weather_data):
    # Check if there is data to process
    if not weather_data:
        print(f"No data available for {city} to store.")
        return

    # Calculate aggregates based on single or limited entries
    temperatures = [entry['temperature'] for entry in weather_data]
    avg_temp = round((sum(temperatures) / len(temperatures)) - 273.15,2)
    max_temp = round(max(temperatures) - 273.15, 2)
    min_temp = round(min(temperatures) - 273.15, 2)

    # Determine the dominant weather condition
    conditions = [entry['main_condition'] for entry in weather_data]
    dominant_condition = Counter(conditions).most_common(1)[0][0]

    # Define the date for the summary
    summary_date = datetime.now().date()

    # Store the daily summary in the database
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO daily_summary (date, city, avg_temp, max_temp, min_temp, dominant_condition)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (summary_date, city, avg_temp, max_temp, min_temp, dominant_condition))
    conn.commit()
    conn.close()

    # print(f"Stored daily summary for {city} on {summary_date}")


threading.Thread(target=schedule_weather_data, daemon=True).start()

# Route to display latest fetched weather data
@app.route('/')
def index():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT city FROM weather_data")
    cities = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template('index.html', cities=cities)

@app.route('/temperature_data')
def temperature_data():
    city = request.args.get('city')
    period = request.args.get('period', 'daily')  # Default to daily if not provided
    data = fetch_temperature_data(city, period)
    return jsonify(data)
# Route to get weather data for a specific city
@app.route('/weather_data')
def get_weather_data():
    city = request.args.get('city')
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute("SELECT * FROM weather_data WHERE city = ? ORDER BY timestamp DESC LIMIT 1", (city,))
    weather_record = c.fetchone()
    conn.close()
    if weather_record:
        data = {
            'city': weather_record[1],
            'temperature': weather_record[2],
            'feels_like': weather_record[3],
            'main_condition': weather_record[4],
            'timestamp': weather_record[5]
        }
        return jsonify(data)
    else:
        return jsonify({'error': 'No data found for the selected city'}), 404

@app.route('/weather_summary')
def weather_summary():
    conn = sqlite3.connect('weather.db')
    c = conn.cursor()
    c.execute('''
        SELECT city, date(timestamp), 
            ROUND(AVG(temperature), 2) as avg_temp,
            ROUND(MAX(temperature), 2) as max_temp,
            ROUND(MIN(temperature), 2) as min_temp,
            (SELECT main_condition 
                FROM weather_data 
                WHERE date(timestamp) = date(w.timestamp)
                GROUP BY main_condition 
                ORDER BY COUNT(*) DESC LIMIT 1) as dominant_condition
        FROM weather_data w
        GROUP BY city, date(timestamp)
    ''')
    summary = c.fetchall()
    conn.close()

    data = []
    for row in summary:
        data.append({
            'city': row[0],
            'date': row[1],
            'avg_temp': row[2],
            'max_temp': row[3],
            'min_temp': row[4],
            'dominant_condition': row[5]
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
