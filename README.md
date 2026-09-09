## 🌤️ Weather Dashboard

Ứng dụng dự báo thời tiết hiện đại với giao diện web đẹp, sử dụng API Open-Meteo (miễn phí, không cần API key).

## ✨ Tính năng

- ✅ Dự báo thời tiết hiện tại
- ✅ Dự báo theo giờ (24 giờ)
- ✅ Dự báo 7 ngày
- ✅ Tìm kiếm thành phố
- ✅ Giao diện responsive (mobile-friendly)
- ✅ Không cần API key
- ✅ Cập nhật realtime

## 🚀 Cài đặt & Chạy

### 1. Clone Repository
```bash
git clone https://github.com/phimmoi123/nguonc.git
cd nguonc
```

### 2. Cài Dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy Weather Dashboard
```bash
python weather_app.py
```

Mở trình duyệt: **http://localhost:5000**

## 📂 Cấu trúc Project (Weather Dashboard)

```
weather/
├── weather_app.py          # Flask server chính
├── weather_api.py          # Module API thời tiết (Open-Meteo)
├── templates/
│   └── weather.html        # HTML template
├── static/
│   ├── style.css           # CSS styling
│   └── script.js           # JavaScript logic
└── requirements.txt        # Dependencies
```

## 🎯 Hướng dẫn sử dụng

### Tìm kiếm thời tiết
1. Nhập tên thành phố trong ô tìm kiếm
2. Nhấn "Tìm kiếm" hoặc Enter
3. Xem dự báo thời tiết chi tiết

### Các thông tin hiển thị
- 🌡️ **Nhiệt độ hiện tại**
- 💧 **Độ ẩm**
- 💨 **Tốc độ gió**
- ☔ **Lượng mưa**
- 📝 **Mô tả thời tiết** (quang đãng, mây, mưa, tuyết, giông...)
- ⏰ **Dự báo theo giờ**
- 📅 **Dự báo 7 ngày**

## 🔧 Customization

### Thay đổi thành phố mặc định
Sửa trong `weather_app.py` line 71:
```python
window.addEventListener('load', () => {
    searchWeatherWithCity('Thành phố của bạn');
});
```

### Thay đổi port
Sửa trong `weather_app.py` line 66:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Thay 5000 thành 8000
```

## 📡 API Endpoints

### GET `/api/weather`
Lấy thời tiết của thành phố
```
GET /api/weather?city=Hà Nội
```

**Response:**
```json
{
  "city": "Hà Nội",
  "current": {
    "temperature": 28.5,
    "humidity": 75,
    "wind_speed": 5.2,
    "precipitation": 0,
    "description": "Có mây",
    "icon": "☁️",
    "time": "2024-01-15T14:30:00"
  },
  "hourly": {...},
  "daily": {...}
}
```

### GET `/api/search`
Tìm kiếm thành phố
```
GET /api/search?q=Hà
```

## 🌐 Open-Meteo API

- **URL:** https://open-meteo.com/
- **Docs:** https://open-meteo.com/en/docs
- **Ưu điểm:**
  - ✅ Miễn phí, không cần API key
  - ✅ Chính xác, được cập nhật thường xuyên
  - ✅ Có geocoding (tìm tọa độ từ tên thành phố)
  - ✅ Hỗ trợ Vietnamese

## 🎨 Giao diện

- **Background:** Gradient tím (667eea → 764ba2)
- **Cards:** Trắng với box-shadow
- **Responsive:** Tối ưu cho mobile, tablet, desktop
- **Icons:** Emoji (tiết kiệm bandwidth)

## 📱 Tương thích

- ✅ Chrome/Edge
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## 🐛 Troubleshooting

### "Không tìm thấy thành phố"
- Kiểm tra lại tên thành phố (viết đúng chính tả)
- Sử dụng tên Việt: "Hà Nội", "TP.HCM", "Đà Nẵng"

### Kết nối lỗi
- Kiểm tra internet connection
- Restart server: `python weather_app.py`

### Port đã được sử dụng
Sử dụng port khác:
```bash
# Sửa trong weather_app.py port=8000
python weather_app.py
```

## 📦 Dependencies

```
requests==2.31.0      # HTTP client
beautifulsoup4==4.12.2  # Web scraping
lxml==4.9.3           # XML parser
flask==3.0.0          # Web framework
flask-cors==4.0.0     # CORS support
```

## 📝 License

MIT License

---

## 🎬 Stremio Addon (Phim Nguồn C)

Repository này cũng bao gồm:
- **addon.py** - Stremio addon server
- **scraper.py** - Script cào phim

Chạy addon:
```bash
python addon.py
```

Thêm vào Stremio: `http://localhost:5000/manifest.json`

---

**Made with ❤️ | Weather Dashboard + Stremio Addon**
