from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# Open-Meteo API
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Weather Dashboard API"}), 200

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', '').strip()
    
    if not city:
        return jsonify({"error": "Vui lòng nhập tên thành phố"}), 400
    
    try:
        # Geocoding - lấy tọa độ từ tên thành phố
        geo_response = requests.get(GEOCODING_URL, params={
            'name': city,
            'count': 1,
            'language': 'vi',
            'format': 'json'
        }, timeout=5)
        
        geo_data = geo_response.json()
        
        if not geo_data.get('results'):
            return jsonify({"error": f"Không tìm thấy thành phố: {city}"}), 404
        
        location = geo_data['results'][0]
        latitude = location['latitude']
        longitude = location['longitude']
        city_name = location.get('name', city)
        
        # Lấy thời tiết
        weather_response = requests.get(WEATHER_URL, params={
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,precipitation',
            'hourly': 'temperature_2m,weather_code,precipitation',
            'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum',
            'timezone': 'Asia/Ho_Chi_Minh',
            'language': 'vi'
        }, timeout=5)
        
        weather_data = weather_response.json()
        
        # Parse current weather
        current = weather_data['current']
        current_data = {
            'temperature': current['temperature_2m'],
            'humidity': current['relative_humidity_2m'],
            'wind_speed': current['wind_speed_10m'],
            'precipitation': current['precipitation'],
            'description': get_weather_description(current['weather_code']),
            'icon': get_weather_icon(current['weather_code']),
            'time': current['time']
        }
        
        # Parse hourly forecast (next 24 hours)
        hourly = weather_data['hourly']
        hourly_data = {
            'times': hourly['time'][:24],
            'temperatures': hourly['temperature_2m'][:24],
            'descriptions': [get_weather_description(code) for code in hourly['weather_code'][:24]],
            'precipitation': hourly['precipitation'][:24]
        }
        
        # Parse daily forecast (7 days)
        daily = weather_data['daily']
        daily_data = {
            'dates': daily['time'],
            'max_temps': daily['temperature_2m_max'],
            'min_temps': daily['temperature_2m_min'],
            'descriptions': [get_weather_description(code) for code in daily['weather_code']],
            'precipitation': daily['precipitation_sum']
        }
        
        return jsonify({
            'city': city_name,
            'current': current_data,
            'hourly': hourly_data,
            'daily': daily_data
        }), 200
        
    except requests.Timeout:
        return jsonify({"error": "Timeout kết nối API"}), 408
    except Exception as e:
        return jsonify({"error": f"Lỗi: {str(e)}"}), 500

@app.route('/api/search', methods=['GET'])
def search_cities():
    q = request.args.get('q', '').strip()
    
    if len(q) < 2:
        return jsonify({"results": []}), 200
    
    try:
        response = requests.get(GEOCODING_URL, params={
            'name': q,
            'count': 10,
            'language': 'vi',
            'format': 'json'
        }, timeout=5)
        
        data = response.json()
        results = []
        
        if data.get('results'):
            for result in data['results']:
                display = result.get('name', '')
                if result.get('admin1'):
                    display += f", {result['admin1']}"
                if result.get('country'):
                    display += f", {result['country']}"
                
                results.append({
                    'name': result.get('name', ''),
                    'display': display,
                    'latitude': result['latitude'],
                    'longitude': result['longitude']
                })
        
        return jsonify({"results": results}), 200
        
    except Exception as e:
        return jsonify({"results": []}), 200

def get_weather_description(code):
    """WMO Weather interpretation codes"""
    descriptions = {
        0: "Quang đãng",
        1: "Chủ yếu quang đãng",
        2: "Có mây",
        3: "Mây che phủ",
        45: "Sương mù",
        48: "Sương mù lạnh",
        51: "Mưa nhỏ",
        53: "Mưa vừa",
        55: "Mưa lớn",
        61: "Mưa nhỏ",
        63: "Mưa vừa",
        65: "Mưa lớn",
        71: "Tuyết nhỏ",
        73: "Tuyết vừa",
        75: "Tuyết lớn",
        80: "Mưa rào nhỏ",
        81: "Mưa rào vừa",
        82: "Mưa rào lớn",
        85: "Tuyết rào nhỏ",
        86: "Tuyết rào lớn",
        95: "Giông có tuyết",
        96: "Giông có mưa đá nhỏ",
        99: "Giông có mưa đá lớn"
    }
    return descriptions.get(code, "Không xác định")

def get_weather_icon(code):
    """Get emoji icon for weather code"""
    if code == 0 or code == 1:
        return "☀️"
    elif code == 2:
        return "🌤️"
    elif code == 3:
        return "☁️"
    elif code in [45, 48]:
        return "🌫️"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return "🌧️"
    elif code in [71, 73, 75, 85, 86]:
        return "🌨️"
    elif code in [95, 96, 99]:
        return "⛈️"
    else:
        return "🌤️"

if __name__ == '__main__':
    app.run(debug=True)
