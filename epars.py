# Imports required
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# main page url
url= 'https://www.ema.europa.eu/en/medicines/ema_group_types/ema_medicine'

def get_data(url):
    #takes each page and returns the text from the response
    r = requests.get(url)
    return r.text

def get_pages(data):
    #using the r.text from the get_data function, creates a soup and works out how many pages are needed to complete the scrape
    soup = BeautifulSoup(data, 'html.parser')
    total = soup.find('h3', {'class': 'ecl-heading'}).text.replace(' ','').replace('results','').strip()
    return round(int(total) / 25, 0)

def parse(data):
    #parse and return data in a list of dicts. 
    eparlist = []
    soup = BeautifulSoup(data, 'html.parser')
    epars = soup.find_all('li', {'class': 'ecl-list-item'})
    for epar in epars:
        myepar = {
            'title': epar.find('h3', {'class': 'ecl-list-item__title'}).text.strip().replace('\n','').replace(' ',''),
            'link': 'https://www.ema.europa.eu' + str(epar.find('a', {'class': 'ecl-link ecl-list-item__link'})['href']),
            'desc': epar.find('div', {'class': 'ema-u-color-grey-2 ecl-u-mb-s'}).text.replace('\n','').replace(' ','').strip()
        }
        eparlist.append(myepar)
    return eparlist 

def output(results):
    # concat the list of list of dicts into a single dataframe for exporting nb - not the tidiest solution.
    resultsdf = pd.concat([pd.DataFrame(g) for g in results])
    resultsdf.to_csv('epars.csv', index=False)    
    return

#run our functions and output the data
results = []
data = get_data(url)
pages = int(get_pages(data))
for x in range(1, 10):
    get_data(f'https://www.ema.europa.eu/en/medicines/ema_group_types/ema_medicine?page={x}')
    results.append(parse(data))
    print('Getting page: ', x)
    time.sleep(1)

output(results)

