import json
import re
import requests
from collections import OrderedDict
from bs4 import BeautifulSoup

response = requests.get('https://www.splendia.com/sitemap/sitemap.xml')

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml-xml')
    
    link = ''
    for i in soup.find_all('loc'):
        if '-property' in i.text and '-en' in i.text:
            link = i.text
            break
     
    response_2 = requests.get(link)
    if response_2.status_code == 200:
        soup = BeautifulSoup(response_2.text, 'lxml-xml')

        link_list = []
        for i in soup.find_all('loc'):
            link_list.append(i.text)
        
        new_data = []
        for i in link_list[:10]:
            response_3 = requests.get(i)            
            soup = BeautifulSoup(response_3.text, "html.parser")
            result = OrderedDict()                   
            p = soup.find_all('p', class_='') 
            result['Title'] = soup.select('h1.heading-1')[0].text.strip()
            result['WHAT WE LOVE'] = re.sub(' +', ' ', p[2].text.strip().replace('\n', ''))
            result['HOTEL DESCRIPTION'] = p[3].text.strip().replace('\n', '')
            new_data.append(result)
        print(new_data)

with open('new_splendia.json', 'w') as fout:
    json.dump(new_data, fout)
