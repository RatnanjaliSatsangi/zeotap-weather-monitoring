document.addEventListener("DOMContentLoaded", function () {
    let countdownTimer = document.getElementById("countdown-timer");
    let fetchInterval = 300; // 5 minutes in seconds
    let timeLeft = fetchInterval;
    let currentUnit = 'C'; // Default unit is Celsius

    function updateCountdown() {
        countdownTimer.textContent = timeLeft;
        if (timeLeft > 0) {
            timeLeft--;
        } else {
            timeLeft = fetchInterval;
        }
    }

    setInterval(updateCountdown, 1000);

    let citySelectForm = document.getElementById("city-select-form");
    citySelectForm.addEventListener("submit", function (event) {
        event.preventDefault();
        let selectedCity = document.getElementById("city-select").value;
        fetchWeatherData(selectedCity);
        fetchTemperatureData(selectedCity); // Fetch default daily temperature data
    });

    function fetchWeatherData(city) {
        fetch(`/weather_data?city=${city}`)
            .then(response => response.json())
            .then(data => {
                displayWeatherData(data);
            })
            .catch(error => console.error('Error fetching weather data:', error));
    }

    function displayWeatherData(data) {
        let weatherContainer = document.getElementById("weather-container");
        if (data.error) {
            weatherContainer.innerHTML = `<p>${data.error}</p>`;
        } else {
            const temperature = convertTemperature(data.temperature);
            const feelsLike = convertTemperature(data.feels_like);

            weatherContainer.innerHTML = `
                <div class="weather-card">
                    <h3>${data.city}</h3>
                    <p>Temperature: ${temperature} °${currentUnit}</p>
                    <p>Feels Like: ${feelsLike} °${currentUnit}</p>
                    <p>Main Condition: ${data.main_condition}</p>
                    <p>Timestamp: ${data.timestamp}</p>
                </div>
            `;
        }
    }

    function fetchTemperatureData(city) {
        const period = document.getElementById("time-period-select").value;
        fetch(`/temperature_data?city=${city}&period=${period}`)
            .then(response => response.json())
            .then(data => {
                const temperatures = data.temperatures.map(temp => convertTemperature(temp));
                renderChart(data.labels, temperatures);
            })
            .catch(error => console.error('Error fetching temperature data:', error));
    }

    const ctx = document.getElementById('temperatureChart').getContext('2d');
    let temperatureChart;

    function renderChart(labels, temperatures) {
        if (temperatureChart) {
            temperatureChart.destroy();
        }

        temperatureChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: `Temperature (°${currentUnit})`,
                    data: temperatures,
                    borderColor: 'blue',
                    fill: false
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: 'Date/Time' } },
                    y: { title: { display: true, text: `Temperature (°${currentUnit})` } }
                }
            }
        });
    }

    // Convert temperature based on the selected unit
    function convertTemperature(tempCelsius) {
        return currentUnit === 'F'
            ? ((tempCelsius * 9) / 5 + 32).toFixed(2)
            : tempCelsius.toFixed(2);
    }

    // Listen for unit changes and update the display
    document.getElementById("unit-select").addEventListener("change", function () {
        currentUnit = this.value;

        // Update the weather data display with new unit
        const selectedCity = document.getElementById("city-select").value;
        fetchWeatherData(selectedCity);

        // Update the chart with the new unit
        fetchTemperatureData(selectedCity);
    });

    const defaultCity = document.getElementById("city-select").value;
    fetchWeatherData(defaultCity);
    fetchTemperatureData(defaultCity);

    document.getElementById("city-select").addEventListener("change", function () {
        const selectedCity = this.value;
        fetchWeatherData(selectedCity);
        fetchTemperatureData(selectedCity);
    });

    document.getElementById("time-period-select").addEventListener("change", function () {
        const selectedCity = document.getElementById("city-select").value;
        fetchTemperatureData(selectedCity);
    });
});
