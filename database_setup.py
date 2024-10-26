# database_setup.py
import sqlite3

def setup_database():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    # Create table for storing real-time weather data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            timestamp INTEGER,
            main_condition TEXT,
            temp REAL,
            feels_like REAL
        )
    ''')

    # Create table for storing daily summaries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            date TEXT,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
