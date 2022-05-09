import os
import requests
import requests
from bs4 import BeautifulSoup
import json
import pandas

url = 'https://www.astraotoshop.com/catalogsearch/result/?'
site = 'https://www.astraotoshop.com/'
params = {'q' : 'ban'}
headers = {'User Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
res = requests.get(url, params=params, headers=headers)
#print(res.headers)
#soup = BeautifulSoup(res.text,'html.parser')
#print(soup.prettify())

def get_total_pages():
    params = {'q' : 'ban'}
    res = requests.get(url, params=params, headers=headers)
    try:
        os.mkdir('aos_output')
    except FileExistsError:
        pass
    with open('aos_output/response.html', 'w+') as ouput:
        ouput.write(res.text)
        ouput.close()
    total_pages = []
    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('ul', 'items pages-items')
    pages = pagination.find_all('li')
    for page in pages:
        total_pages.append(page.text)
    total = int(max(total_pages))
    return total


def get_all_item():
    params = {'q': 'ban'}
    res = requests.get(url, params=params, headers=headers)
    try:
        os.mkdir('aos_output')
    except FileExistsError:
        pass
    with open('aos_output/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()
    soup = BeautifulSoup(res.text, 'html.parser')
    #proses scraping
    contents = soup.find_all('ol', 'products')
    produk_list = []
    for item in contents:
        produk = item.find('strong', 'product')
        sku = item.find('p', 'product-sku')
        harga = item.find('span', 'special-price')
        try:
            produk_link = site + produk.find('a') ['href']
        except:
            produk_link = 'Link Produk tidak ditemukan'
        #Sort Data by Dict
        data_dict = {
            'Produk': produk,
            'SKU': sku,
            'Harga': harga,
            'Link Produk': produk_link
        }
        produk_list.append(data_dict)
        #Export to json
        with open('aos_output/produk_list.json', 'w+') as produk_json:
                json.dump(produk_list, produk_json)
        print(produk_list)




if __name__ == '__main__':
    get_all_item()








