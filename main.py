from crawler import crawl_data
from database import init_db, save_to_db

if __name__ == "__main__":
    init_db()
    songs = crawl_data(max_pages=4)
    if songs:
        save_to_db(songs)
        print(f"Đã lưu {len(songs)} bài hát vào cơ sở dữ liệu.")
    else:
        print("Không lấy được bài hát nào.")
