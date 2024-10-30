import requests as REQS
from bs4 import BeautifulSoup as BS4

# CONSTANTS
NUMBER_OF_PAGES_TO_SEARCH = 20

"""
    function scrape_zameen(city: str, pages_range: int) -> list:
    - this function will scrape the zameen.com website and return a list of information regarding houses.
        :param city: str
        :param pages_range: int
        :return: list
"""
def scrape_zameen(city: str, pages_range: int) -> list:
    HOUSES_INFO = []
    for PAGE in range((pages_range + 1)):
        URL = f'https://www.zameen.com/Homes/{city}-{PAGE}.html'
        print(URL)
        RESPONSE = REQS.get(URL)
        CONTENT = BS4(RESPONSE.text, 'html.parser')
        HOUSES_LIST = CONTENT.select('main > div > div > div> div > ul > li')
        PREV_LEN = len(HOUSES_LIST)
        
        for HOUSE in HOUSES_LIST:
            BATHROOMS = HOUSE.select_one("span[aria-label='Baths']")
            BEDROOMS = HOUSE.select_one("span[aria-label='Beds']")
            LOCATION = HOUSE.select_one("div[aria-label='Location']")
            PRICE = HOUSE.select_one("span[aria-label='Price']")
            SIZE = HOUSE.select_one("div[title]>div > div > span:nth-child(1)")
            
            if PRICE:
                if SIZE is None:
                    SIZE = LOCATION.parent.select_one(
                        "div:nth-child(2) > div > span:nth-child(3)"
                    )
                HOUSES_INFO.append(
                    {
                        'location': text(LOCATION),
                        'price': text(PRICE, datatype = 'num'),
                        'bedrooms': text(BEDROOMS, datatype = 'num'),
                        'baths': text(BATHROOMS, datatype = 'num'),
                        'size': text(SIZE, datatype = 'size')
                    }
                )
        if len(HOUSES_INFO) == PREV_LEN:
            break
    return HOUSES_INFO

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
                'info': scrape_zameen(f"{CITY.get('name')}-{CITY.get('id')}", NUMBER_OF_PAGES_TO_SEARCH)
            }
        )
    
    # TODO: implementation of taking data & writing to CSV file.