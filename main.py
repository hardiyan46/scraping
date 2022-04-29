import os
import requests
from bs4 import BeautifulSoup

url = 'https://id.indeed.com/jobs'
params = {
    'q' : 'python developer',
    'l' : 'jakarta',
    'vjk' : 'b8bc9c3e08bc8ae3'
}
headers = {'User Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
res = requests.get(url, params=params, headers=headers)
#print(res.headers)
soup = BeautifulSoup(res.text,'html.parser')
print(soup.prettify())

def get_total_pages():
    params = {
        'q': 'python developer',
        'l': 'jakarta',
        'vjk': 'b8bc9c3e08bc8ae3'
    }

    res = requests.get(url, params=params, headers=headers)
    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()


