from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Hàm lấy dữ liệu bài hát từ cơ sở dữ liệu với phân trang
def get_songs(page=1, per_page=30, search_query=None, db_path="MyMusic.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tính toán offset để lấy dữ liệu phù hợp với trang hiện tại
    offset = (page - 1) * per_page

    # Thực hiện truy vấn với điều kiện tìm kiếm và phân trang
    if search_query:
        search = f"%{search_query}%"
        cursor.execute("""
            SELECT song_name, singer_names, image_url, link_page 
            FROM songs 
            WHERE song_name LIKE ? OR singer_names LIKE ?
            LIMIT ? OFFSET ?
        """, (search, search, per_page, offset))
    else:
        cursor.execute("""
            SELECT song_name, singer_names, image_url, link_page 
            FROM songs 
            LIMIT ? OFFSET ?
        """, (per_page, offset))
    
    data = cursor.fetchall()
    
    # Lấy tổng số bài hát để tính số trang
    cursor.execute("SELECT COUNT(*) FROM songs")
    total_songs = cursor.fetchone()[0]
    conn.close()
    
    total_pages = (total_songs + per_page - 1) // per_page  # Tính số trang

    return data, total_pages

@app.route("/", methods=["GET"])
def home():
    # Trang chủ sẽ chuyển hướng đến trang introduce
    return redirect(url_for('introduce'))

@app.route("/introduce", methods=["GET"])
def introduce():
    return render_template("introduce.html")

@app.route("/thamkhao", methods=["GET"])
def thamkhao():
    return render_template("thamkhao.html")

@app.route("/index", methods=["GET"])
def index():
    query = request.args.get("search", "")
    page = int(request.args.get("page", 1))  # Mặc định trang 1
    songs, total_pages = get_songs(page, search_query=query)
    
    return render_template("index.html", songs=songs, search=query, page=page, total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)