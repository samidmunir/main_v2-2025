import requests as REQS
from bs4 import BeautifulSoup as BS4

# CONSTANTS
NUMBER_OF_PAGES_TO_SEARCH = 20

def scrape_web():
    pass

if __name__ == '__main__':
    HOUSE_DATA = []
    
    CITIES = [
        {'id': 1, 'name': 'Gujranwala'},
        {'id': 2, 'name': 'Islamabad'},
        {'id': 3, 'name': 'Karachi'},
        {'id': 4, 'name': 'Lahore'},
        {'id': 5, 'name': 'Multan'},
        {'id': 6, 'name': 'Murree'},
        {'id': 7, 'name': 'Peshawar'}
    ]
    
    for CITY in CITIES:
        HOUSE_DATA.append(
            {
                'city': CITY.get('name'),
                'info': scrape_web(f"{CITY.get('name')}-{CITY.get('id')}", NUMBER_OF_PAGES_TO_SEARCH)
            }
        )