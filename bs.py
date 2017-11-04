from bs4 import BeautifulSoup as soup

import urllib3

import csv

from datetime import datetime

import pandas as pd

import numpy as np

http = urllib3.PoolManager()
url = 'https://geo.craigslist.org/iso/us/'

r = http.request('GET', url)

## This are for quick data checking
## --------------------------
print(r.status)
#print(r.headers)
#print(r.data)
##--------------------------

## Start of Beautiful Soup

response = soup(r.data, "html.parser")
#print(response.prettify())

# to get all ul
#ul_lists = response.find_all('ul')


# Filter UL we want
city_lists = response.find_all('ul', {'class': 'height6'})



#print(city_lists)


city_dict = {}

for city in city_lists[0].find_all('a'):
    city_dict[city.text] = city.attrs['href']


#for key, value in city_dict.items():
#    print(key, value)


sf_url = city_dict['inland empire, CA']

print(sf_url)

full_url = sf_url + '/search/sya'

search_params = {
    'query': 'linux',
    'min_price': '100',
    'max_price': '400',
   }

r = http.request('GET', full_url, fields=search_params)

print(r.status)

resp = soup(r.data, "html.parser")

#print(resp.prettify())

data = []

data_subset = resp.find_all('p', attrs={'class': 'result-info'})

for data_row in data_subset:
    title_lists = data_row.find('a', attrs={'class': 'result-title hdrlnk'})
    price_lists = data_row.find('span', attrs={'class': 'result-price'})
    place_lists = data_row.find('span', attrs={'class': 'result-hood'})

    if place_lists is None:
        place_lists = data_row.find('span', attrs={'class': 'nearby'})

    if title_lists is None:
        title_text = " "
    else:
        title_text = title_lists.text.strip()

    if price_lists is None:
        price_val = " "
    else:
        price_val = price_lists.text.strip()

    if place_lists is None:
        places_val = " "
    else:
        places_val = place_lists.text.strip()

    data.append((title_text, price_val, places_val))

    print(title_text, price_val, places_val)


with open('rakcheck.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for title, price, places in data:
        writer.writerow([title, price, places, datetime.now()])


index = 0

df = pd.DataFrame(columns=('title', 'price', 'city'), index=np.arange(0, 40*len(data)))

for title, price, places in data:
    df.loc[index] = [title, price, places]
    index += 1

# Quick check of value - First 5
# df.head()
# Quick check of info
# df.info()
# quick check of stats
# df.describe()

print(df.describe())

#for title, price, places in zip(title_lists, price_lists, place_lists):
#    title_text = title.text.strip()
#    price_val = price.text.strip()
#    places_val = places.text.strip()
#    print(title_text, price_val, places_val)
#    data.append((title_text, price_val, places_val))
