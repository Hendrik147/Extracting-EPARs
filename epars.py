# from helium import *
import requests
from bs4 import BeautifulSoup

url= 'https://www.ema.europa.eu/en/medicines/ema_group_types/ema_medicine'
page = requests.get(url)

# browser = start_chrome(url)

# if Text('I accept cookies').exists():
#     click("I accept cookies")

# while Text('LOAD MORE').exists():
#     click('LOAD MORE')
#     time.sleep(4)
#     if not Text('LOAD MORE').exists(): break


epar_name_list = BeautifulSoup.find(class_ ='ema-listings view-content-solr ecl-u-pt-m')
epar_name_list_items = epar_name_list.find_all('a')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

def get_data(url):
    r = requests.get(url)
    data = dict(r.json())
    return data

def parse(data):    
    # Pull all titles and descriptions
    for epar_name in epar_name_list_items:
        title = epar_name.find(class_='ecl-list-item__title ecl-heading').text.strip()
        link = "https://www.ema.europa.eu" + epar_name.get('href')
        description = epar_name.find(class_='ema-u-color-grey-2 ecl-u-mb-s').text.strip()
        myepar = {
                'title': title,
                'link': link,
                'description': description
        }
    return myepar

def output(results):
    myepar.to_csv('epars.csv', index=False)    
    return

results = []
data = get_data(url)
results(parse(data))
output(results)

