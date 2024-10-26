# weather_api.py
import requests

API_KEY = '0bc5a9f095fc73b3bbdd623c2f314324'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Cities of interest
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def kelvin_to_celsius(temp_k):
    return temp_k - 273.15

def fetch_weather_data(city):
    """Fetch weather data for a given city from OpenWeatherMap API."""
    url = f"{BASE_URL}?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        main = data['weather'][0]['main']
        temp = kelvin_to_celsius(data['main']['temp'])
        feels_like = kelvin_to_celsius(data['main']['feels_like'])
        timestamp = data['dt']
        
        return {
            'city': city,
            'main': main,
            'temp': temp,
            'feels_like': feels_like,
            'timestamp': timestamp
        }
    else:
        print(f"Error fetching data for {city}: {data}")
        return None

# Example call
if __name__ == "__main__":
    for city in CITIES:
        weather = fetch_weather_data(city)
        print(weather)
