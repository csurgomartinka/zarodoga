import requests
from bs4 import BeautifulSoup
import json


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
'''
'https://www.programturizmus.hu/kategoria-fesztival.html',              #ez működik
'https://www.programturizmus.hu/kategoria-vasarok.html',                #elvileg működik
'https://www.programturizmus.hu/kategoria-unnepek.html',                #elvileg jó
'https://www.programturizmus.hu/kategoria-szabadido.html',              #elvileg jó
'https://www.programturizmus.hu/kategoria-kulturalis-program.html',     #elvileg jó
'https://www.programturizmus.hu/kategoria-csalad-gyerek.html',          #elvileg jó
'https://www.programturizmus.hu/kategoria-gasztronomiai-program.html',  #elvileg jó
'https://www.programturizmus.hu/kategoria-rendezveny.html'              #elvileg jó
'''

varosok = requests.get("http://localhost:3000/varosLista")
esemenyek = requests.get("http://localhost:3000/esemenyLista")
varosokjol = json.loads(varosok.text)
esemenyekjol = json.loads(esemenyek.text)
#for a in varosokjol:
    #print(a)

#esemeny    - helyszinid
#helyszin   - helyszin_nev varosid

tipusid = 1

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
                print(b) #esemény dátuma
            h3 = a.find('h3')
            nev = h3.find('a')
            #print(nev)
            event_name = nev.get_text(strip=True)
            event_link = "https://www.programturizmus.hu" + nev['href']
            #helyszin = requests.get(event_link)
            #helyszin_soup = BeautifulSoup(helyszin.text, 'html.parser')
            #destination_div = helyszin_soup.find('div', class_='destination-address')
            #print(destination_div)
            #print(event_link)
            for c in nev:
                print(c) #esemény címe
            varosdiv = a.find('div',class_='tourism_path_list')
            #print(varosdiv)
            for k in varosdiv:
                for l in k:
                    #print(l)
                    varosa = l.find('a')
                    if "telepules" in str(varosa):
                        for o in varosa:
                            print(o) #esemény városa
                            for p in varosokjol:
                                #print(p)
                                #{'vnev': 'Villány'}
                                #print("{\'vnev\': \'" + o + "\'}")
                                if("{\'vnev\': \'" + o + "\'}" == str(p)):
                                    print("találat")         #helyszinnek a város idja                        
            leiras = a.find('p',class_='tourism-descrition')
            #print(leiras)
            for e in leiras:
                print(e) #esemény leírás
        except:
            print("")
        
        #tipusid hozzáadása
        print(tipusid) #esemény tipusának idja
        print("--------------------------------------------------------------------------------------------------------------------------------------")
    tipusid += 1
    
        
        
        

