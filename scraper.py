import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class PhimNguoncScraper:
    def __init__(self):
        self.base_url = "https://phim.nguonc.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_movies(self, page=1):
        """Cào danh sách phim từ trang chủ"""
        try:
            url = f"{self.base_url}/danh-sach/phim-moi?page={page}"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"Lỗi: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            movies = []
            
            # Tìm các phim trong danh sách
            film_items = soup.find_all('div', class_='film-poster-container')
            
            for item in film_items:
                try:
                    title_elem = item.find('h3', class_='film-name')
                    link_elem = item.find('a', class_='film-poster-link')
                    poster_elem = item.find('img')
                    
                    if title_elem and link_elem:
                        movie = {
                            'title': title_elem.text.strip(),
                            'url': link_elem.get('href', ''),
                            'poster': poster_elem.get('src', '') if poster_elem else '',
                            'id': link_elem.get('href', '').split('/')[-1],
                        }
                        
                        # Đảm bảo URL đầy đủ
                        if movie['url'] and not movie['url'].startswith('http'):
                            movie['url'] = self.base_url + movie['url']
                        
                        movies.append(movie)
                except Exception as e:
                    print(f"Lỗi xử lý phim: {e}")
                    continue
            
            return movies
        
        except Exception as e:
            print(f"Lỗi cào dữ liệu: {e}")
            return []
    
    def get_movie_details(self, movie_url):
        """Lấy chi tiết phim"""
        try:
            response = requests.get(movie_url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Tìm thông tin phim
            title = soup.find('h1', class_='film-name')
            description = soup.find('div', class_='film-description')
            
            details = {
                'title': title.text.strip() if title else '',
                'description': description.text.strip() if description else '',
                'url': movie_url,
            }
            
            # Tìm link phát
            play_button = soup.find('a', class_='play-button')
            if play_button:
                stream_url = play_button.get('href', '')
                if stream_url and not stream_url.startswith('http'):
                    stream_url = self.base_url + stream_url
                details['stream_url'] = stream_url
            
            return details
        
        except Exception as e:
            print(f"Lỗi lấy chi tiết: {e}")
            return None
    
    def save_to_json(self, movies, filename='movies.json'):
        """Lưu dữ liệu vào file JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(movies, f, ensure_ascii=False, indent=2)
            print(f"✓ Lưu {len(movies)} phim vào {filename}")
        except Exception as e:
            print(f"Lỗi lưu file: {e}")

if __name__ == "__main__":
    scraper = PhimNguoncScraper()
    
    print("🎬 Đang cào dữ liệu từ phim.nguonc.com...")
    
    # Cào 3 trang đầu
    all_movies = []
    for page in range(1, 4):
        print(f"Cào trang {page}...")
        movies = scraper.get_movies(page)
        all_movies.extend(movies)
        print(f"  Tìm thấy {len(movies)} phim")
    
    print(f"\n✓ Tổng cộng: {len(all_movies)} phim")
    scraper.save_to_json(all_movies)
