import requests
from bs4 import BeautifulSoup

url = 'https://www.astraotoshop.com/catalogsearch/result/?'
params = {
    'q' : 'ban vario'

}
headers = {'User Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
res = requests.get(url, params=params, headers=headers)
#print(res.headers)
soup = BeautifulSoup(res.text,'html.parser')
print(soup.prettify())
