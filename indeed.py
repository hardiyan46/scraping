import os
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://id.indeed.com/jobs'
site = 'https://id.indeed.com'
params = {
    'q': 'python developer',
    'l': 'jakarta',
    'vjk': 'b8bc9c3e08bc8ae3'
}
headers = {'User Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'}
res = requests.get(url, params=params, headers=headers)
"""
print(res.headers)
Scraping step
soup = BeautifulSoup(res.text,'html.parser')
print(soup.prettify())
"""


def get_total_pages(query, location):
    params = {
        'q': query,
        'l': location,
        'vjk': 'b8bc9c3e08bc8ae3'
    }
    res = requests.get(url, params=params, headers=headers)
    #create folder dan file
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
    print(total_pages)
    total = int(max(total_pages))
    return total


def get_items(query, location, start, page):
    params = {
        'q': query,
        'l': location,
        'start': start,
        'vjk': 'b8bc9c3e08bc8ae3'
    }
    res = requests.get(url, params=params, headers=headers)
    with open('temp/res.html', "w", encoding="utf-8") as outfile:
        outfile.write(res.text)
        outfile.close()
    soup = BeautifulSoup(res.text, 'html.parser')
#Scraping proses
    contents = soup.find_all('table', 'jobCard_mainContent')
    job_list = []
    for item in contents:
        title = item.find('h2', 'jobTitle').text
        company = item.find('span','companyName')
        company_name = company.text
        try:
            company_link = site + company.find('a')['href']
        except:
            company_link = 'Link Tidak Ditemukan'
        #sorting data by dictionary
        data_dict = {
            'Title': title,
            'Company Name': company_name,
            'Link': company_link
        }
        job_list.append(data_dict)
    #export to json
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass
    with open('json_result/job_list.json', 'w+') as json_data:
        json.dump(job_list, json_data)
    return job_list
   #print('File Json sudah dibuat')

"""
    #export to csv
    df = pd.DataFrame(job_list)
    df.to_csv('indeed_data.csv', index=False)
    df.to_excel('indeed_data.xlsx', index=False)
    print('Export csv dan excel berhasil')
"""
#Create document for dynamic scraping
def create_document(dataframe, filename):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass

    df = pd.DataFrame(dataframe)
    df.to_csv(f'data_result/{filename}.csv', index=False)
    df.to_excel(f'data_result/{filename}.xlsx', index=False)

    print(f'File {filename}.csv dan {filename}.xlsx Berhasil dibuat ')


#create Function Run
def run():
    query = input('Masukan Key pencarian : ')
    location = input('Masukan lokasi :')

    total = get_total_pages(query, location)
    counter = 0
    final_result = []
    for page in range(total):
        page += 1
        counter += 10
        final_result += get_items(query, location, counter, page)

        ##formating data
    try:
        os.mkdir('reports')
    except FileExistsError:
        pass

    with open('reports/{}.json'. format(query), 'w+') as final_data:
        json.dump(final_result, final_data)
    print('Data Json sudah dibuat')

    #Create Document
    create_document(final_result, query)


if __name__ == '__main__':
    run()
