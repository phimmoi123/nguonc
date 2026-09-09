from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from weather_api import WeatherAPI
import json

app = Flask(__name__)
CORS(app)

weather_api = WeatherAPI()

@app.route('/')
def index():
    """Trang chủ dashboard"""
    return render_template('weather.html')

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """API lấy thời tiết"""
    city = request.args.get('city', 'Hà Nội')
    
    try:
        # Lấy tọa độ từ tên thành phố
        coords = weather_api.get_coordinates(city)
        
        if not coords:
            return jsonify({
                'error': f'Không tìm thấy thành phố "{city}"'
            }), 404
        
        # Lấy dữ liệu thời tiết
        weather = weather_api.get_weather(
            coords['latitude'],
            coords['longitude'],
            coords['name']
        )
        
        if not weather:
            return jsonify({
                'error': 'Lỗi lấy dữ liệu thời tiết'
            }), 500
        
        return jsonify(weather)
    
    except Exception as e:
        print(f"Lỗi: {e}")
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/search', methods=['GET'])
def search_city():
    """Tìm kiếm thành phố"""
    query = request.args.get('q', '')
    
    if not query or len(query) < 2:
        return jsonify({'results': []})
    
    try:
        coords = weather_api.get_coordinates(query)
        
        if coords:
            return jsonify({
                'results': [{
                    'name': coords['name'],
                    'country': coords['country'],
                    'display': f"{coords['name']}, {coords['country']}"
                }]
            })
        
        return jsonify({'results': []})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    print("🌤️ Weather Dashboard server starting...")
    print("📍 http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
