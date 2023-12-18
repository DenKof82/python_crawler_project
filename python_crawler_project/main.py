
import requests # HTTP užklausoms atlikti
from bs4 import BeautifulSoup  # HTML turinio analizei
import pandas as pd  # duomenų analizei ir CSV failų kūrimui
import time  # laiko matavimui
import os  # operacinės sistemos funkcionalumo (failų kūrimui) naudojimui

def download_image(image_url, folder_path, file_name):
    response = requests.get(image_url)  # Atliekame HTTP GET užklausą į nurodytą nuotraukos URL
    if response.status_code == 200:  # Jeigu užklausa sėkminga (HTTP statusas 200)
        file_path = os.path.join(folder_path, file_name)  # Sukuriame pilną failo kelią
        with open(file_path, 'wb') as file:  # Atidarome failą rašymui ('wb' rašymas baitais)
            file.write(response.content)  # Įrašome gautą turinį į failą
        return file_path  # Grąžiname sukurtą failo kelią
    return None  # Grąžiname 'None', jei užklausa nesėkminga

def crawl_vitamin_c_products(time_limit, source, return_format, download_images=False):
    start_time = time.time()  # Fiksuojame funkcijos pradžios laiką
    data = {'product_name': [], 'price': [], 'image_url': [], 'image_path': []}  # Sukuriame tuščią duomenų žodyną
    image_folder = 'downloaded_images'  # Nurodome aplanko pavadinimą nuotraukoms saugoti

    if download_images and not os.path.exists(image_folder):  # Jeigu reikia atsisiųsti nuotraukas ir aplankas neegzistuoja
        os.makedirs(image_folder)  # Sukuriame aplanką

    try:
        response = requests.get(source)  # Atliekame HTTP GET užklausą į nurodytą šaltinį
        if response.status_code != 200:  # Jeigu užklausa nesėkminga
            return "Failed to retrieve data from the source"  # Grąžiname klaidos pranešimą

        soup = BeautifulSoup(response.content, 'html.parser')  # Analizuojame gautą HTML turinį su BeautifulSoup

        for product in soup.find_all('div', class_='product product-item product-item-31286'):  # Perrenkame per visus produktus (pagal HTML klasę)
            product_name = product.find('h3', class_='product__title').text.strip()  # Ištraukiame produkto pavadinimą
            price = product.find('span', class_='product__price--regular').text.strip()  # Ištraukiame produkto kainą
            #image_url = product.find('img')['src']  # Ištraukiame nuotraukos URL

            data['product_name'].append(product_name)  # Įdedame pavadinimą į duomenų žodyną
            data['price'].append(price)  # Įdedame kainą į duomenų žodyną
            #data['image_url'].append(image_url)  # Įdedame nuotraukos URL į duomenų žodyną

            #if download_images:  # Jeigu reikia atsisiųsti nuotraukas
                #image_path = download_image(image_url, image_folder, f"{product_name}.jpg")  # Atsisiunčiame nuotrauką
                #data['image_path'].append(image_path)  # Įdedame nuotraukos vietinį kelią į duomenų žodyną

            if time.time() - start_time > time_limit:  # Jeigu viršijamas nurodytas laiko limitas
                break  # Nutraukiame ciklą

    except Exception as e:
        return str(e)  # Jeigu įvyksta klaida, grąžiname klaidos pranešimą

    if return_format == 'csv':  # grąžinimo formatas yra CSV
        return pd.DataFrame(data).to_csv(index=False)  # Konvertuojame duomenis į DataFrame ir grąžiname kaip CSV
    else:
        return data  # Priešingu atveju, grąžiname duomenis kaip žodyną

# Pavyzdinis funkcijos iškvietimas
result = crawl_vitamin_c_products(
    time_limit=100,
    source="https://www.gintarine.lt/search?q=c+vitaminai",
    return_format='csv',
    #download_images=True
)
print(result)