# visualizations.py
import sqlite3
import matplotlib.pyplot as plt

def plot_daily_summary(city):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date, avg_temp, max_temp, min_temp
        FROM daily_summary
        WHERE city = ?
    ''', (city,))

    data = cursor.fetchall()
    dates = [row[0] for row in data]
    avg_temps = [row[1] for row in data]
    max_temps = [row[2] for row in data]
    min_temps = [row[3] for row in data]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, avg_temps, label='Avg Temp')
    plt.plot(dates, max_temps, label='Max Temp')
    plt.plot(dates, min_temps, label='Min Temp')
    
    plt.title(f'Daily Temperature Summary for {city}')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_daily_summary('Delhi')
