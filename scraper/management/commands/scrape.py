# importing the required modules
import numpy as np
import requests
import xml.etree.ElementTree as ET
import time
import urllib.request
import extruct
from w3lib.html import get_base_url
from scraper.models import Product
from django.db import IntegrityError
from fake_useragent import UserAgent
import sys
from bs4 import BeautifulSoup

start_time = time.time()
ua = UserAgent()
#UCWEB/2.0 (compatible; Googlebot/2.1; +google.com/bot.html)
headers = {
    "User-Agent": ua.random,
    'Referer': 'www.google.com'
}

# url of rss feed
url = 'https://www.tinte24.de/sitemap/devices.xml'
req = urllib.request.Request(
    url=url,
    data=None,
    headers=headers
)
#response = urllib.request.urlopen(req).read()
response = requests.get(url, headers=headers, timeout=5)

root = ET.fromstring(response.text)
urls_to_scrape = []
i = 0

for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    #i = i + 1
    loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    urls_to_scrape.append(loc)
    #if '/Tinte/' in loc:
    #    urls_to_scrape.append(loc)
    #if '/Toner/' in loc:
    #    urls_to_scrape.append(loc)

urls_to_scrape = list(set(urls_to_scrape))
#print(f'Scrapovat sa bude {len(urls_to_scrape)} produktov z celkoveho poctu {i}')
print(f'Scrapovat sa bude {len(urls_to_scrape)} produktov')
j = 0

for url_to_scrape in urls_to_scrape:
    data_list = []
    #cached_url = 'http://webcache.googleusercontent.com/search?q=cache:' + url_to_scrape
    j = j + 1
    print(f'Starting scraping {j}/{len(urls_to_scrape)} url: {url_to_scrape}')
    try:
        #print(ua.random)
        r = requests.get(url_to_scrape, headers=headers, timeout=5)
        #print(r.text)
        soup = BeautifulSoup(r.content, 'html.parser')
    except:
        sys.exit("Cant load website. Check connection.")
    base_url = get_base_url(r.text, r.url)
    data = extruct.extract(r.text, base_url=base_url, uniform=True, syntaxes=['rdfa', 'json-ld'])
    data_list = data['json-ld']
    print(data_list)

    if data_list == []:
        sys.exit("Website did not respond correctly, quitting")
    for data_dict in data_list:
        compatible = soup.find("div", class_='compatible')
        print('kompatibilne s ', compatible)
        brand=color=depth=gtin12=logo=manufacturer=mpn=sku=alternateName=description=image=name = ''
        price = data_dict['offers']['price']
        priceCurrency = data_dict['offers']['priceCurrency']
        try:
            name = data_dict['name']
            image = data_dict['image']
            url = data_dict['offers']['url']
            brand = data_dict['brand']
            color = data_dict['color']
            depth = data_dict['depth']
            gtin12 = data_dict['gtin12']
            logo = data_dict['logo']
            manufacturer = data_dict['manufacturer']
            mpn = data_dict['mpn']
            sku = data_dict['sku']
            alternateName = data_dict['alternateName']
            description = data_dict['description']

        except:
            print('cant get all parameters')

        availability = data_dict['offers']['availability']
        if 'InStock'.lower() in availability.lower():
            availability = "In stock"
        elif 'OutOfStock'.lower() in availability.lower():
            availability = "Out Of Stock"
        elif 'PreOrder'.lower() in availability.lower():\
            availability = "Preorder"
        else:
            availability = ""
            print("cant get availability")
        print('dostupnost je ', availability)
        itemCondition = data_dict['offers']['itemCondition']
        if 'NewCondition'.lower() in itemCondition.lower():
            itemCondition = "New"
        elif 'UsedCondition'.lower() in itemCondition.lower():
            itemCondition = "Used Condition"
        elif 'RefurbishedCondition'.lower() in itemCondition.lower():
            itemCondition = "Refurbished Condition"
        elif 'DamagedCondition'.lower() in itemCondition.lower():
            itemCondition = "Damaged Condition"
        else:
            itemCondition = ""
        if name != '':
            try:
                p = Product(availability=availability, itemCondition=itemCondition, price=price, priceCurrency=priceCurrency,
                            url=url, brand=brand, color=color, depth=depth, gtin12=gtin12, logo=logo,
                            manufacturer=manufacturer, mpn=mpn, sku=sku, alternateName=alternateName, description=description,
                            image=image, name=name, compatible=compatible)
                p.save()
                print('ulozene')
            except IntegrityError:
                print("Cant scrape already existing url ", url_to_scrape)
                pass
        else:
            pass

    print(f'Scrapnute {j} produktov z celkoveho poctu {len(urls_to_scrape)}')
    delays = [7, 24, 22, 12, 30, 19]
    delay = np.random.choice(delays)
    print('waiting ',delay)
    time.sleep(delay)


    #except:
    #    print("Cant scrape url ", url_to_scrape)



finish_time = time.time()
elapsed_time = finish_time - start_time
print(f'Skript bezal {elapsed_time} sekund.')
