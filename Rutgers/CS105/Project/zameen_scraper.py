import requests as REQS
from bs4 import BeautifulSoup as BS4

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