import requests
import sys
import urllib.parse
import json
import time
import os

def debug_response(search_term, offset=0, limit=20):
    base_url = "https://api.wallapop.com/api/v3/general/search"
    params = {
        "keywords": search_term.replace(' ','%20'), # Weird wallapop encoding
        "longitude": -5,
        "latitude": 37,
        "sold": "True",
        "offset": offset,
        "limit": limit
    }
    # Manually encode parameters except for the search term
    encoded_params = urllib.parse.urlencode({k: v for k, v in params.items() if k != 'keywords'})
    url = f"{base_url}?keywords={search_term}&{encoded_params}"
    headers = {
        "Accept": "*/*",
        "User-Agent": "Wget/1.21.4",
        "Accept-Encoding": "identity",
        "X-DeviceOS": "0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("API Error: HTTP", response.status_code)
        print("Response:", response.text)
        return None
    return response.json()

def extract_products(search_term: str, offset=0, limit = 20, hard_limit = 100):
    '''
    Extracts products from Wallapop API
    :param search_term: str, search term
    :param offset: int, page number
    :param limit: int, number of items
    :param hard_limit: int, final number of products
    '''
    all_products = []
    while True:
        # Clear the console and show the current offset
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Current offset: {offset} / {hard_limit}")

        data = debug_response(search_term, offset, limit)
        if data is None or "search_objects" not in data:
            break
        products = data['search_objects']
        if not products:
            break
        all_products.extend(products)
        # If fewer objects are received than the limit, it is the last page
        if len(products) < limit:
            break
        offset += limit
        time.sleep(1)  # Short pause to avoid saturating the API
        
        if hard_limit < offset:
            break

    return all_products