import requests
from bs4 import BeautifulSoup
import json
import mysql.connector
import time
import os


# URL listája
urls = [
    'https://www.programturizmus.hu/kategoria-fesztival.html',
    'https://www.programturizmus.hu/kategoria-vasarok.html',
    'https://www.programturizmus.hu/kategoria-unnepek.html',
    'https://www.programturizmus.hu/kategoria-szabadido.html',
    'https://www.programturizmus.hu/kategoria-kulturalis-program.html', 
    'https://www.programturizmus.hu/kategoria-csalad-gyerek.html',
    'https://www.programturizmus.hu/kategoria-gasztronomiai-program.html',
    'https://www.programturizmus.hu/kategoria-rendezveny.html'
]

varosok = requests.get("http://localhost:3000/varosLista")
esemenyek = requests.get("http://localhost:3000/esemenyLista")
varosokjol = json.loads(varosok.text)
esemenyekjol = json.loads(esemenyek.text)
#for a in varosokjol:
    #print(a)


try:
    requests.delete("http://localhost:3000/helyszinTorles")
    requests.delete("http://localhost:3000/esemenyTorles")
    #requests.delete("http://localhost:3000/varosTorles")
except:
    print("üres tábla")

tipusid = 1
varososid = 1

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='esemenyek'
)
cursor = conn.cursor()

# URL-ek feldolgozása
for url in urls:
    print(f"Feldolgozás: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Események keresése
    events = soup.find_all('div', class_='tourism-list destination-list has-list-order')
    esemeny = soup.find_all('div',class_='tourism-list-item')
    #print(esemeny[0])
    for a in esemeny:
        datum = a.find('span',class_='tourism_time')
        #print(datum)
        try:
            for b in datum:
                #print(b) #esemény dátuma
                datumki = b
            h3 = a.find('h3')
            nev = h3.find('a')
            #print(nev)
            event_name = nev.get_text(strip=True)
            event_link = "https://www.programturizmus.hu" + nev['href']
            helyszin = requests.get(event_link)
            helyszin_soup = BeautifulSoup(helyszin.text, 'html.parser')
            destination_div = helyszin_soup.find('div', class_='destination-address')
            reszletek_div = helyszin_soup.find('div', id='destination-text')
            reszletek = reszletek_div.get_text(separator='\n', strip=True)
            if reszletek == "":
                reszletek = "Hiányzó"
            
            #print(reszletek_div)
            #print(destination_div)
            #print(reszletek)

            if destination_div:
                all_text = destination_div.get_text(separator=" ", strip=True)
            
            city_link = destination_div.find('a')
            if city_link:
                city_name = city_link.get_text(strip=True)
            #print("Város:", city_name)

            street_name = None
            if "," in all_text:
                parts = all_text.split(',')
            if len(parts) > 1:
                street_name = parts[1].strip()
            if '(' in street_name:
                street_name = street_name.split('(')[0].strip()
            if street_name:
                print("Utca:", street_name)
            else:
                street_name = "Nincs megadva"


            if "Több helyszínen" in all_text:
                helyszin_szoveg = "Több helyszínen"
                #print(helyszin_szoveg)
            
            varososidja = 0
            varososid = 1
            
            for q in varosokjol:
                #print(q)
                #if("{\'vnev\': \'" + city_name + "\'}" == str(q)):
                if q.get('vnev') == city_name:
                    varososidja = varososid
                varososid += 1
            if varososidja == 0:
                felvitel = "http://localhost:3000/varosFelvitel"
                response = requests.post(felvitel, json={"vnev":city_name}) #timeout=30
                os.system('taskkill /F /IM node.exe')
                time.sleep(2)
                os.system('start node C:\\Users\\diak\\Desktop\\szoftver\\VNA\\24_zarodoga\\backend\\zarodoga_backend\\backend.js')
                varosok = requests.get("http://localhost:3000/varosLista")
                varosokjol = json.loads(varosok.text)
                varososidja = varososid
                if response.status_code == 200:
                    print(f"Sikeres feltöltés")
                else:
                    print(f"Hiba történt: {response.status_code}")

            #print(event_link)
            for c in nev:
                print(c) #esemény címe
                nevki = c
            varosdiv = a.find('div',class_='tourism_path_list')
            #print(varosdiv)
            for k in varosdiv:
                for l in k:
                    #print(l)
                    varosa = l.find('a')
                    if "telepules" in str(varosa):
                        for o in varosa:
                            idja = 0
                            #print(o) #esemény városa
                            for p in varosokjol:
                                idja += 1
                                #print(p.get('vnev'))
                                #print(o)
                                #{'vnev': 'Villány'} várososid
                                #print("{\'vnev\': \'" + o + "\'}")
                                if p.get('vnev') == o:
                                    #print("találat")         
                                    #print(idja)                 
                                    varosid = idja
            leiras = a.find('p',class_='tourism-descrition')
            #print(leiras)
            for e in leiras:
                #print(e) #esemény leírás
                leiraski = e

            esemenyTabla =  {
                'nev': nevki,
                'datum': datumki,
                'varosid': varosid,
                'tipusid': tipusid,
                'leiras': leiraski,
                'reszletek':reszletek
            }
    
            felvitel = "http://localhost:3000/esemenyFelvitel"
            session = requests.Session()

            response = requests.post(felvitel, json=esemenyTabla) #timeout=30
            if response.status_code == 200:
                print(f"Sikeres feltöltés")
            else:
                print(f"Hiba történt: {response.status_code}")
            
            utolsoidurl = "http://localhost:3000/esemenyUtolsoID"
            response = requests.get(utolsoidurl)
            if response.status_code == 200:
                utolsoid = response.json()
                esemenyid = utolsoid[0].get('id')
            print(varososidja)
            helyszinTabla =  {
                'helyszin_nev': street_name,
                'varosid': varososidja,
                'esemenyid': esemenyid
            }
    
            helyszinfelvitel = "http://localhost:3000/helyszinFelvitel"
            session = requests.Session()

            response = requests.post(helyszinfelvitel, json=helyszinTabla) #timeout=30
            if response.status_code == 200:
                print(f"Sikeres feltöltés")
            else:
                print(f"Hiba történt: {response.status_code}")
            
        except:
            print("")
        
        #tipusid hozzáadása
        print(tipusid) #esemény tipusának idja

        

        '''
        print(nevki)
        print(datumki)
        print(varosid)
        print(tipusid)
        print(leiraski)
        print(reszletek)
        '''
       
        print("--------------------------------------------------------------------------------------------------------------------------------------")
    tipusid += 1
     

