// DOM Elements
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const suggestions = document.getElementById('suggestions');
const loading = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const currentWeatherDiv = document.getElementById('currentWeather');
const hourlySection = document.getElementById('hourlySection');
const dailySection = document.getElementById('dailySection');

// Event Listeners
searchBtn.addEventListener('click', searchWeather);
searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchWeather();
});
searchInput.addEventListener('input', handleSuggestions);

// Load default weather on page load
window.addEventListener('load', () => {
    searchWeatherWithCity('Hà Nội');
});

// Search weather by city
async function searchWeather() {
    const city = searchInput.value.trim();
    if (!city) {
        showError('Vui lòng nhập tên thành phố');
        return;
    }
    
    suggestions.innerHTML = '';
    searchWeatherWithCity(city);
}

// Search with specific city
async function searchWeatherWithCity(city) {
    showLoading(true);
    hideError();

    try {
        const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
        
        if (!response.ok) {
            const data = await response.json();
            showError(data.error || 'Không tìm thấy thành phố');
            showLoading(false);
            return;
        }

        const weather = await response.json();
        displayWeather(weather);
        searchInput.value = weather.city;
        
    } catch (error) {
        showError('Lỗi: ' + error.message);
        console.error('Error:', error);
    } finally {
        showLoading(false);
    }
}

// Handle city suggestions
async function handleSuggestions(e) {
    const query = e.target.value.trim();
    
    if (query.length < 2) {
        suggestions.innerHTML = '';
        return;
    }

    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.results && data.results.length > 0) {
            displaySuggestions(data.results);
        } else {
            suggestions.innerHTML = '';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Display suggestions
function displaySuggestions(results) {
    suggestions.innerHTML = results.map(result => `
        <div class="suggestion-item" onclick="selectCity('${result.name}')">
            📍 ${result.display}
        </div>
    `).join('');
}

// Select city from suggestions
function selectCity(city) {
    searchInput.value = city;
    suggestions.innerHTML = '';
    searchWeatherWithCity(city);
}

// Display weather data
function displayWeather(weather) {
    const current = weather.current;

    // Update current weather
    document.getElementById('cityName').textContent = weather.city;
    document.getElementById('updateTime').textContent = `Cập nhật: ${formatTime(current.time)}`;
    document.getElementById('temp').textContent = Math.round(current.temperature || 0);
    document.getElementById('weatherIcon').textContent = current.icon;
    document.getElementById('description').textContent = current.description;
    document.getElementById('humidity').textContent = `${current.humidity || '--'}%`;
    document.getElementById('windSpeed').textContent = `${(current.wind_speed || '--')} km/h`;
    document.getElementById('precipitation').textContent = `${(current.precipitation || 0)} mm`;

    currentWeatherDiv.style.display = 'block';

    // Display hourly forecast
    displayHourlyForecast(weather.hourly);

    // Display daily forecast
    displayDailyForecast(weather.daily);
}

// Display hourly forecast
function displayHourlyForecast(hourly) {
    const hourlyForecast = document.getElementById('hourlyForecast');
    
    hourlyForecast.innerHTML = hourly.times.map((time, index) => `
        <div class="hourly-item">
            <div class="hourly-time">${formatHourTime(time)}</div>
            <div class="hourly-icon">${getWeatherIcon(hourly.descriptions[index])}</div>
            <div class="hourly-temp">${Math.round(hourly.temperatures[index] || 0)}°</div>
            <div class="hourly-desc">${hourly.descriptions[index] || '--'}</div>
        </div>
    `).join('');

    hourlySection.style.display = 'block';
}

// Display daily forecast
function displayDailyForecast(daily) {
    const dailyForecast = document.getElementById('dailyForecast');
    
    dailyForecast.innerHTML = daily.dates.map((date, index) => `
        <div class="daily-item">
            <div class="daily-date">${formatDate(date)}</div>
            <div class="daily-icon">${getWeatherIcon(daily.descriptions[index])}</div>
            <div class="daily-temps">
                <div class="daily-max">${Math.round(daily.max_temps[index] || 0)}°</div>
                <div class="daily-min">${Math.round(daily.min_temps[index] || 0)}°</div>
            </div>
            <div class="daily-desc">${daily.descriptions[index] || '--'}</div>
            <div class="daily-precip">☔ ${(daily.precipitation[index] || 0)} mm</div>
        </div>
    `).join('');

    dailySection.style.display = 'block';
}

// Get weather icon by description
function getWeatherIcon(description) {
    if (!description) return '🌤️';
    
    description = description.toLowerCase();
    
    if (description.includes('quang đãng') || description.includes('trời quang')) return '☀️';
    if (description.includes('mây')) return '☁️';
    if (description.includes('sương mù')) return '🌫️';
    if (description.includes('mưa')) return '🌧️';
    if (description.includes('tuyết')) return '🌨️';
    if (description.includes('giông')) return '⛈️';
    
    return '🌤️';
}

// Format time for display
function formatTime(time) {
    if (!time) return '--';
    const date = new Date(time);
    return date.toLocaleString('vi-VN');
}

// Format hour time
function formatHourTime(time) {
    if (!time) return '--';
    const date = new Date(time);
    return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
}

// Format date
function formatDate(date) {
    if (!date) return '--';
    const dateObj = new Date(date);
    const days = ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'];
    const day = dateObj.getDay();
    const dayName = days[day];
    const dayNum = dateObj.getDate();
    const month = dateObj.getMonth() + 1;
    
    return `${dayName} ${dayNum}/${month}`;
}

// Show loading
function showLoading(show) {
    loading.style.display = show ? 'block' : 'none';
}

// Show error
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Hide error
function hideError() {
    errorDiv.style.display = 'none';
}
