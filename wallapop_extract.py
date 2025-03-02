import requests
import sys
import urllib.parse
import json
import time

def debug_response(search_term, offset=0, limit=20):
    base_url = "https://api.wallapop.com/api/v3/general/search"
    params = {
        "keywords": search_term,
        "longitude": -3.69196,
        "latitude": 40.41956,
        "offset": offset,
        "limit": limit
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    print(url)
    headers = {
        "Accept": "*/*",
        "User-Agent": "Wget/1.21.4",
        "Accept-Encoding": "identity",
        "X-DeviceOS": "0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error en la API: HTTP", response.status_code)
        print("Respuesta:", response.text)
        return None
    return response.json()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_query = sys.argv[1]
    else:
        search_query = input("Introduce la búsqueda (por ejemplo, 'iphone x'): ")
    
    search_query = search_query.replace(' ','%20')
    
    print(search_query)
    
    offset = 0 # page number
    limit = 40 # number of items
    hard_limit = 100 # final number of products
    all_products = []
    while True:
        data = debug_response(search_query, offset, limit)
        if data is None or "search_objects" not in data:
            break
        products = data['search_objects']
        if not products:
            break
        all_products.extend(products)
        # Si se reciben menos objetos que el límite, es la última página
        if len(products) < limit:
            break
        offset += limit
        time.sleep(1)  # Pequeña pausa para evitar saturar la API
        
        if hard_limit < offset:
        	break

    for product in all_products:
        print(product['title'], 
              # product['distance'], 
              product['price'])