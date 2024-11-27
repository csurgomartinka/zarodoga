import requests
from bs4 import BeautifulSoup
import json
import time
import schedule
from datetime import datetime

# URL, amelyről az adatokat le szeretnénk tölteni
url = 'https://csodalatosmagyarorszag.hu/kategoria/programok/'



# User-Agent beállítása a kéréshez
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch_and_save_events():
    # Az oldal lekérése a megadott User-Agent fejléc használatával
    response = requests.get(url, headers=headers)

    # Ellenőrizzük a válasz státuszkódját
    if response.status_code != 200:
        print(f"Hiba történt: {response.status_code}")
    else:
        # Az oldal HTML kódja
        soup = BeautifulSoup(response.text, 'html.parser')

        # Keresés az eseményekre (például a post-shadow osztályú article-ök)
        events = soup.find_all('article', class_='post shadow col mb20 n100')

        # Ha nem találunk eseményeket
        if not events:
            print("Nem találhatóak események.")
        else:
            # Események adatainak kinyerése
            event_list = []
            for event in events:
                event_data = {}

                # Dátum kinyerése
                date = event.find('h4', class_='post_date date_badge bred mb10')
                if date:
                    event_data['date'] = date.get_text(strip=True)

                # Cím kinyerése
                title = event.find('h3', class_='post_title fs24px mb20 cdgrey')
                if title:
                    event_data['title'] = title.get_text(strip=True)

                # Helyszín kinyerése
                location = event.find('h4', class_='post_city fs14px ib cblack')
                if location:
                    event_data['location'] = location.get_text(strip=True)

                # Az adatokat hozzáadjuk az események listájához
                if event_data:
                    event_list.append(event_data)

            # Frissítés dátumának rögzítése
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # JSON fájlba mentés a 'var tomb =' szintaxissal
            with open('events_data.json', 'w', encoding='utf-8') as json_file:
                # Írás a fájlba: 'var tomb = ' + JSON struktúra
                json_file.write(f"var tomb = {json.dumps(event_list, ensure_ascii=False, indent=4)};\n")

            print(f"{len(event_list)} eseményt találtunk, és sikeresen kiírtuk a 'events_data.json' fájlba.")

# Feladat ütemezése
schedule.every().day.at("00:00").do(fetch_and_save_events)

# A scheduler futtatása
while True:
    schedule.run_pending()  # Ellenőrzi, hogy van-e futtatandó feladat
    time.sleep(1)  # Vár egy kicsit, hogy ne terhelje a CPU-t
