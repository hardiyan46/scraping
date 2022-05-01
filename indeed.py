import os
import requests
from bs4 import BeautifulSoup

url = 'https://id.indeed.com/jobs'
site = 'https://id.indeed.com'
params = {
    'q' : 'python developer',
    'l' : 'jakarta',
    'vjk' : 'b8bc9c3e08bc8ae3'
}
headers = {'User Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
res = requests.get(url, params=params, headers=headers)
#print(res.headers)
#Scraping step
#soup = BeautifulSoup(res.text,'html.parser')
#print(soup.prettify())

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
    with open('temp/res.html', "w", encoding="utf-8") as outfile:
        outfile.write(res.text)
        outfile.close()
    total_pages = []
    #Scarping step
    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('ul', 'pagination-list')
    pages = pagination.find_all('li')
    for page in pages:
        total_pages.append(page.text)
    total = int(max(total_pages))
    return total



def get_items():
    params = {
        'q': 'python developer',
        'l': 'jakarta',
        'vjk': 'b8bc9c3e08bc8ae3'
    }
    res = requests.get(url, params=params, headers=headers)
    with open('temp/res.html', "w", encoding="utf-8") as outfile:
        outfile.write(res.text)
        outfile.close()
    soup = BeautifulSoup(res.text, 'html.parser')

#Scraping proses
    contents = soup.find_all('table', 'jobCard_mainContent')


    for item in contents:
        title = item.find('h2', 'jobTitle').text
        company = item.find('span','companyName')
        company_name = company.text
        try:
            company_link = site + company.find('a') ['href']
        except:
            company_link = 'Link Tidak Ditemukan'

        data_dict = {
            'Title' : title,
            'Company Name' : company_name,
            'Link' : company_link
        }
        print(data_dict)


if __name__ == '__main__':
    get_items()

