import requests
import json
from datetime import datetime, timedelta

class WeatherAPI:
    """Open-Meteo Weather API (Free, no API key needed)"""
    
    BASE_URL = "https://api.open-meteo.com/v1"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'WeatherDashboard/1.0'
        }
    
    def get_coordinates(self, city):
        """Lấy tọa độ từ tên thành phố"""
        try:
            url = f"{self.BASE_URL}/geocoding"
            params = {
                'name': city,
                'count': 1,
                'language': 'vi',
                'format': 'json'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('results'):
                result = data['results'][0]
                return {
                    'latitude': result['latitude'],
                    'longitude': result['longitude'],
                    'name': result['name'],
                    'country': result.get('country', ''),
                    'admin1': result.get('admin1', '')
                }
            return None
        
        except Exception as e:
            print(f"Lỗi lấy tọa độ: {e}")
            return None
    
    def get_weather(self, latitude, longitude, city_name=""):
        """Lấy dữ liệu thời tiết hiện tại"""
        try:
            url = f"{self.BASE_URL}/forecast"
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,precipitation',
                'hourly': 'temperature_2m,weather_code,precipitation',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum',
                'temperature_unit': 'celsius',
                'wind_speed_unit': 'kmh',
                'precipitation_unit': 'mm',
                'timezone': 'auto',
                'forecast_days': 7
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return self._parse_weather(data, city_name)
        
        except Exception as e:
            print(f"Lỗi lấy thời tiết: {e}")
            return None
    
    def _parse_weather(self, data, city_name):
        """Parse dữ liệu thời tiết"""
        current = data.get('current', {})
        hourly = data.get('hourly', {})
        daily = data.get('daily', {})
        
        weather = {
            'city': city_name,
            'current': {
                'temperature': current.get('temperature_2m'),
                'humidity': current.get('relative_humidity_2m'),
                'wind_speed': current.get('wind_speed_10m'),
                'precipitation': current.get('precipitation', 0),
                'description': self._get_weather_description(current.get('weather_code')),
                'icon': self._get_weather_icon(current.get('weather_code')),
                'time': current.get('time')
            },
            'hourly': {
                'temperatures': hourly.get('temperature_2m', [])[:24],
                'times': hourly.get('time', [])[:24],
                'descriptions': [self._get_weather_description(code) for code in hourly.get('weather_code', [])[:24]]
            },
            'daily': {
                'dates': daily.get('time', []),
                'max_temps': daily.get('temperature_2m_max', []),
                'min_temps': daily.get('temperature_2m_min', []),
                'descriptions': [self._get_weather_description(code) for code in daily.get('weather_code', [])],
                'precipitation': daily.get('precipitation_sum', [])
            }
        }
        
        return weather
    
    def _get_weather_description(self, code):
        """Chuyển WMO weather code thành mô tả"""
        weather_codes = {
            0: "Trời quang đãng",
            1: "Quang đãng",
            2: "Ít mây",
            3: "Có mây",
            45: "Có sương mù",
            48: "Sương mù lạnh",
            51: "Mưa nhẹ",
            53: "Mưa vừa",
            55: "Mưa nặng",
            61: "Mưa nhẹ",
            63: "Mưa vừa",
            65: "Mưa nặng",
            71: "Tuyết nhẹ",
            73: "Tuyết vừa",
            75: "Tuyết nặng",
            80: "Mưa rào nhẹ",
            81: "Mưa rào vừa",
            82: "Mưa rào nặng",
            85: "Mưa tuyết nhẹ",
            86: "Mưa tuyết nặng",
            95: "Giông bão",
            96: "Giông bão + mưa đá nhẹ",
            99: "Giông bão + mưa đá nặng"
        }
        return weather_codes.get(code, "Không xác định")
    
    def _get_weather_icon(self, code):
        """Lấy emoji icon cho loại thời tiết"""
        if code == 0:
            return "☀️"
        elif code == 1 or code == 2:
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

if __name__ == "__main__":
    api = WeatherAPI()
    
    # Test: Lấy thời tiết Hà Nội
    coords = api.get_coordinates("Hà Nội")
    if coords:
        print(f"📍 {coords['name']}, {coords['country']}")
        print(f"Tọa độ: {coords['latitude']}, {coords['longitude']}")
        
        weather = api.get_weather(coords['latitude'], coords['longitude'], coords['name'])
        
        if weather:
            current = weather['current']
            print(f"\n🌡️ Hiện tại: {current['temperature']}°C")
            print(f"💧 Độ ẩm: {current['humidity']}%")
            print(f"💨 Gió: {current['wind_speed']} km/h")
            print(f"☔ Mưa: {current['precipitation']} mm")
            print(f"📝 {current['description']} {current['icon']}")
