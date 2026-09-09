from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from scraper import PhimNguoncScraper

app = Flask(__name__)
CORS(app)

# Cấu hình addon
ADDON_NAME = "Nguồn C"
ADDON_ID = "phim.nguonc.stremio"
ADDON_VERSION = "1.0.0"

scraper = PhimNguoncScraper()

# Manifest - mô tả addon cho Stremio
@app.route('/manifest.json')
def manifest():
    return jsonify({
        "id": ADDON_ID,
        "version": ADDON_VERSION,
        "name": ADDON_NAME,
        "description": "Xem phim từ Nguồn C trên Stremio",
        "types": ["movie", "series"],
        "resources": ["catalog", "stream"],
        "catalogs": [
            {
                "type": "movie",
                "id": "phim_moi",
                "name": "Phim Mới"
            },
            {
                "type": "series",
                "id": "series_moi",
                "name": "Series Mới"
            }
        ]
    })

# Catalog - danh sách phim
@app.route('/catalog/<type>/<id>.json')
def catalog(type, id):
    try:
        # Cào dữ liệu từ trang web
        movies = scraper.get_movies(page=1)
        
        # Chuyển đổi sang định dạng Stremio
        metas = []
        for movie in movies:
            meta = {
                "id": movie.get('id', ''),
                "type": type,
                "name": movie.get('title', ''),
                "poster": movie.get('poster', ''),
                "url": movie.get('url', '')
            }
            metas.append(meta)
        
        return jsonify({
            "metas": metas
        })
    except Exception as e:
        print(f"Lỗi catalog: {e}")
        return jsonify({"metas": []})

# Stream - link phát video
@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    try:
        # Cào chi tiết phim
        movies = scraper.get_movies(page=1)
        
        for movie in movies:
            if movie.get('id') == id:
                # Lấy link phát
                details = scraper.get_movie_details(movie.get('url', ''))
                
                if details and details.get('stream_url'):
                    return jsonify({
                        "streams": [
                            {
                                "title": "Phát",
                                "url": details.get('stream_url', ''),
                                "sources": [
                                    {
                                        "url": details.get('stream_url', ''),
                                        "quality": "720p"
                                    }
                                ]
                            }
                        ]
                    })
        
        return jsonify({"streams": []})
    except Exception as e:
        print(f"Lỗi stream: {e}")
        return jsonify({"streams": []})

# Health check
@app.route('/health')
def health():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    print(f"🎬 Khởi động Stremio Addon: {ADDON_NAME}")
    print(f"📍 Addon URL: http://localhost:5000/manifest.json")
    print("\n📲 Thêm vào Stremio: http://localhost:5000/manifest.json")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
