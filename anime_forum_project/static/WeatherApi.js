document.addEventListener("DOMContentLoaded", function() {
    const weatherWidget = document.getElementById('weather');

    function fetchWeather(latitude, longitude) {
        const apiUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                displayWeather(data);
            })
            .catch(error => {
                console.error('Error fetching weather data:', error);
            });
    }

    function displayWeather(data) {
        const weather = data.current_weather;
        const weatherIconUrl = `https://openweathermap.org/img/wn/${getWeatherIcon(weather.weathercode)}.png`;

        weatherWidget.innerHTML = `
            <div class="d-flex align-items-center">
                <img src="${weatherIconUrl}" alt="Weather icon" />
                <div>
                    <p class="mb-0">Current Location</p>
                    <p class="mb-0">${weather.temperature}°C, ${getWeatherDescription(weather.weathercode)}</p>
                </div>
            </div>
        `;
    }

    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(position => {
                const { latitude, longitude } = position.coords;
                fetchWeather(latitude, longitude);
            }, error => {
                console.error('Error getting location:', error);
            });
        } else {
            console.error('Geolocation is not supported by this browser.');
        }
    }
//God forgive me for what I'm about to do
    function getWeatherIcon(weatherCode) {
        const weatherIcons = {
            0: "01d", // Clear sky
            1: "02d", // Mainly clear
            2: "03d", // Partly cloudy
            3: "04d", // Overcast
            45: "50d", // Fog
            48: "50d", // Depositing rime fog
            51: "09d", // Drizzle: Light
            53: "09d", // Drizzle: Moderate
            55: "09d", // Drizzle: Dense
            56: "09d", // Freezing Drizzle: Light
            57: "09d", // Freezing Drizzle: Dense
            61: "10d", // Rain: Slight
            63: "10d", // Rain: Moderate
            65: "10d", // Rain: Heavy
            66: "13d", // Freezing Rain: Light
            67: "13d", // Freezing Rain: Heavy
            71: "13d", // Snow fall: Slight
            73: "13d", // Snow fall: Moderate
            75: "13d", // Snow fall: Heavy
            77: "13d", // Snow grains
            80: "09d", // Rain showers: Slight
            81: "09d", // Rain showers: Moderate
            82: "09d", // Rain showers: Violent
            85: "13d", // Snow showers slight
            86: "13d", // Snow showers heavy
            95: "11d", // Thunderstorm: Slight or moderate
            96: "11d", // Thunderstorm with slight hail
            99: "11d"  // Thunderstorm with heavy hail
        };
        return weatherIcons[weatherCode] || "01d";
    }

    function getWeatherDescription(weatherCode) {
        const weatherDescriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Drizzle: Light",
            53: "Drizzle: Moderate",
            55: "Drizzle: Dense",
            56: "Freezing Drizzle: Light",
            57: "Freezing Drizzle: Dense",
            61: "Rain: Slight",
            63: "Rain: Moderate",
            65: "Rain: Heavy",
            66: "Freezing Rain: Light",
            67: "Freezing Rain: Heavy",
            71: "Snow fall: Slight",
            73: "Snow fall: Moderate",
            75: "Snow fall: Heavy",
            77: "Snow grains",
            80: "Rain showers: Slight",
            81: "Rain showers: Moderate",
            82: "Rain showers: Violent",
            85: "Snow showers: Slight",
            86: "Snow showers: Heavy",
            95: "Thunderstorm: Slight or moderate",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        };
        return weatherDescriptions[weatherCode] || "Clear sky";
    }

    getLocation();
});
