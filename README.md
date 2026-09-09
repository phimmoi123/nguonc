# 🎬 Stremio Nguồn C

Addon Stremio để xem phim từ **phim.nguonc.com**

## ✨ Tính năng

- ✅ Cào danh sách phim mới
- ✅ Tích hợp với Stremio
- ✅ Link phát trực tiếp
- ✅ Hỗ trợ Movies & Series

## 📦 Cài đặt

### 1. Clone Repository
```bash
git clone https://github.com/phimmoi123/nguonc.git
cd nguonc
```

### 2. Cài Dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy Addon
```bash
python addon.py
```

Addon sẽ chạy tại: `http://localhost:5000`

## 🎯 Thêm vào Stremio

1. Mở **Stremio**
2. Vào **Settings** → **Addons**
3. Nhập URL addon: `http://localhost:5000/manifest.json`
4. Nhấn **Install**

## 🔄 Cào Dữ liệu

Chạy scraper độc lập:
```bash
python scraper.py
```

Dữ liệu sẽ được lưu vào `movies.json`

## 📁 Cấu trúc Project

```
nguonc/
├── addon.py           # Addon Stremio server
├── scraper.py         # Script cào dữ liệu
├── requirements.txt   # Dependencies
├── movies.json        # Dữ liệu phim (tự động tạo)
└── README.md          # Hướng dẫn này
```

## 🛠️ Customization

### Thay đổi trang cào
Sửa `base_url` trong `scraper.py`:
```python
self.base_url = "https://phim.nguonc.com"
```

### Thay đổi cấu hình addon
Sửa `addon.py`:
```python
ADDON_NAME = "Tên addon của bạn"
ADDON_ID = "addon.id.custom"
```

## ⚠️ Lưu ý

- Tuân thủ **Terms of Service** của trang web
- Không spam requests
- Cung cấp User-Agent hợp lý

## 📝 License

MIT License

---

**Made with ❤️ for movie lovers**
