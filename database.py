import sqlite3

def init_db(db_name="MyMusic.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_name TEXT,
            singer_names TEXT,
            image_url TEXT,
            link_page TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(songs_data, db_name="MyMusic.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for song_name, singer_names, image_url, link_page in songs_data:
        cursor.execute("""
            INSERT INTO songs (song_name, singer_names, image_url, link_page)
            VALUES (?, ?, ?, ?)
        """, (song_name, singer_names, image_url, link_page))
    conn.commit()
    conn.close()
