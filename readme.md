# Real-Time Weather Monitoring Dashboard

This is a Real-Time Weather Monitoring Dashboard that displays current weather data and historical temperature trends for a selected city. Users can switch between Celsius and Fahrenheit units, view temperature trends over various periods (hourly, daily, weekly, monthly), and see visualizations using Chart.js.

## Table of Contents
1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)
5. [Endpoints](#endpoints)
6. [Code Structure](#code-structure)
7. [Temperature Conversion](#temperature-conversion)
8. [License](#license)

---

## Features

- **Real-Time Weather Data**: Fetches and displays the latest temperature, "feels like" temperature, weather condition, and timestamp for the selected city.
- **Historical Temperature Visualization**: Shows temperature trends with options to view data at hourly, daily, weekly, and monthly intervals.
- **Unit Conversion**: Allows users to toggle between Celsius and Fahrenheit units for all temperature data on the page.
- **City Selection**: Users can select from multiple cities to view specific weather data.
- **Interactive Chart**: Utilizes Chart.js to provide a responsive line chart for temperature trends.

---

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Backend**: Python (Flask)
- **Database**: SQLite
- **API**: OpenWeather API (or similar, configurable)

---

## Setup and Installation

### Prerequisites
- Python 3.x
- Flask (`pip install flask`)
- SQLite (comes with Python)
- Chart.js (included via CDN in HTML)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/weather-monitoring-dashboard.git
   cd weather-monitoring-dashboard
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **API Key Configuration**:
   - Sign up at [OpenWeather](https://openweathermap.org/) (or other weather API providers) to get an API key.
   - Replace `YOUR_API_KEY` in `main.py` with your actual API key.

4. **Database Setup**:
   - Run the `setup_database()` function in `main.py` to create the required SQLite tables (`daily_summaries` and `weather_data`).
   - You can populate the `weather_data` and `daily_summaries` tables manually or through the API if historical data is available.

5. **Run the Application**:
   ```bash
   python main.py
   ```

6. **Access the Application**:
   - Open your browser and go to `http://127.0.0.1:5000`.

---

## Usage

1. **Select City**: Use the dropdown to select a city for which you want to view weather data.
2. **View Current Weather**: The dashboard displays the latest temperature, "feels like" temperature, main weather condition, and timestamp for the selected city.
3. **Temperature Unit Toggle**: Use the unit toggle at the top right to switch between Celsius and Fahrenheit.
4. **Temperature Trend Visualization**: 
   - Select a time period (Hourly, Daily, Weekly, Monthly) using the dropdown below the "Temperature Trends" header.
   - The line chart updates with the temperature trends for the selected period.
5. **Auto-Refresh**: The dashboard refreshes data every 5 minutes by default.

---

## Endpoints

### 1. `/weather_data?city=<city_name>`
- **Method**: GET
- **Description**: Fetches the current weather data for the specified city.
- **Response**: JSON data containing temperature, feels like temperature, main weather condition, and timestamp.

### 2. `/temperature_data?city=<city_name>&period=<time_period>`
- **Method**: GET
- **Description**: Retrieves historical temperature data for the selected city based on the chosen period (hourly, daily, weekly, or monthly).
- **Parameters**:
  - `city`: Name of the city (e.g., `Delhi`).
  - `period`: Granularity of the data (`hourly`, `daily`, `weekly`, `monthly`).
- **Response**: JSON data with labels (dates/times) and temperatures.

---

## Code Structure

### 1. **`main.py`**
   - The main server file with Flask endpoints.
   - Handles API requests to fetch weather data, convert units, and store summaries in the SQLite database.
   - Defines the `/weather_data` and `/temperature_data` endpoints to serve current and historical weather data.
   - `fetch_temperature_data(city, period)`: Fetches data from `weather_data` and `daily_summaries` tables based on the specified period.

### 2. **`index.html`**
   - Contains the HTML structure for the dashboard.
   - Includes the city selector, temperature unit toggle, time period dropdown, and a `canvas` element for the Chart.js line chart.

### 3. **`style.css`**
   - Provides basic styling for the dashboard.
   - Customizes the dropdowns, buttons, and overall layout.

### 4. **`scripts.js`**
   - Contains JavaScript for interactivity, including:
     - Fetching current weather data and displaying it in the UI.
     - Fetching historical temperature data and rendering it in a Chart.js line chart.
     - Converting temperature units between Celsius and Fahrenheit.
     - Handling dropdown changes to update data dynamically.

---

## Temperature Conversion

- **Celsius to Fahrenheit**:
  - Formula: `(°C × 9/5) + 32 = °F`
- **Fahrenheit to Celsius**:
  - Formula: `(°F - 32) × 5/9 = °C`
  
When the user switches between Celsius and Fahrenheit, the JavaScript functions in `scripts.js` convert and update all temperature values on the page and in the chart.
