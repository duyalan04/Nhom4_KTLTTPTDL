import requests
from bs4 import BeautifulSoup

base_url = "https://www.nhaccuatui.com/bai-hat/bai-hat-moi"

def crawl_page(url, page_num):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        song_containers = soup.find_all("div", class_="box-content-music-list")
        songs_data = []

        for container in song_containers:
            song_name = "N/A"
            singer_names = "N/A"
            image_url = "N/A"
            link_page = "N/A"

            name_tag = container.find("a", class_="name_song")
            if name_tag:
                song_name = name_tag.text.strip()
                link_page = name_tag.get("href", "N/A")

            singer_tags = container.find_all("a", class_="name_singer")
            if singer_tags:
                singers = [s.text.strip() for s in singer_tags]
                singer_names = ", ".join(singers)

            img_tag = container.find("img")
            if img_tag and "src" in img_tag.attrs:
                image_url = img_tag["src"]

            if song_name != "N/A" and link_page != "N/A":
                songs_data.append((song_name, singer_names, image_url, link_page))

        return songs_data

    except Exception as e:
        print(f"[ERROR] Page {page_num}: {e}")
        return []

def crawl_data(max_pages=3):
    all_songs = []
    for page in range(1, max_pages + 1):
        page_url = f"{base_url}.html" if page == 1 else f"{base_url}.{page}.html"
        songs_data = crawl_page(page_url, page)
        if not songs_data:
            break
        all_songs.extend(songs_data)
    return all_songs
