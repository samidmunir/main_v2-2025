import requests as REQS
from bs4 import BeautifulSoup as BS4

# CONSTANTS
NUMBER_OF_PAGES_TO_SEARCH = 20

"""
    function convert_price(price: str) -> float:
    - this function converts a given price in crore, lakhs, millions, thousands -> numbers (decimal).
        :param price: str
        :return: float
"""
def convert_price(price: str) -> float:
    if price.endswith('Crore'):
        return round(float(price[:-5]) * 10000000)
    elif price.endswith('Lakh'):
        return round(float(price[:-4]) * 100000)
    elif price.endswith('Million'):
        return round(float(price[:-7]) * 1000000)
    elif price.endswith('Arab'):
        return round(float(price[:-4]) * 1000000000)
    elif price.endswith('Thousand'):
        return round(float(price[:-8]) * 1000)
    else:
        return round(float(price))

"""
    function convert_size(size: str) -> float:
    - this function converts a given size (in kanal & merla) to square footage.
        :param size: str
        :return: float
"""
def convert_size(size: str) -> float:
    if size.endswith('Marla'):
        return round(float(size[:-5].replace(',', '')) * 225)
    elif size.endswith('Kanal'):
        return round(float(size[:-5].replace(',', '')) * 4500)
    elif size.endswith('Sq. Yd.'):
        return round(float(size[:-7].replace(',', '')) * 9)
    else:
        return round(float(size))

"""
    function get_text(tag, data_type = 'str'):
    - this function will return the text of the parameter tag.
        :param tag: tag object
        :param data_type: num, str, price, OR size
        :return: price (number or string)
"""
def get_text(tag, data_type = 'str'):
    if tag is None and data_type == 'num':
        return 0
    if data_type == 'num':
        try:
            return int(tag.text.strip())
        except ValueError:
            return 0
    
    if tag is None and data_type == 'str':
        return ''
    if data_type == 'str':
        return tag.text.strip()
    
    if tag is None and data_type == 'price':
        return 0.0
    if data_type == 'price':
        return convert_price(tag.text.strip())
    
    if tag is None and data_type == 'size':
        return 0.0
    if data_type == 'size':
        return convert_size(tag.text.strip())

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
                        'location': get_text(LOCATION),
                        'price': get_text(PRICE, data_type = 'num'),
                        'bedrooms': get_text(BEDROOMS, data_type = 'num'),
                        'baths': get_text(BATHROOMS, data_type = 'num'),
                        'size': get_text(SIZE, data_type = 'size')
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
    
    with open('zameen_data.csv', 'w') as FILE:
        FILE.write('city|location|price|bedrooms|bathrooms|size\n')
        for HOUSE in HOUSE_DATA:
            for DATA in HOUSE.get('info'):
                FILE.write(
                    f"{HOUSE.get('city')}|{DATA.get('location')}|{DATA.get('price')}|{DATA.get('bedrooms')}|{DATA.get('bathrooms')}|{DATA.get('size')}\n"
                )