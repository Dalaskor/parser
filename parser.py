import requests
from bs4 import BeautifulSoup as bsoup
import time
import logging

URL = 'https://www.fl.ru/search/?type=projects&action=search&search_string=python&search_hint=Next%2Bgen&page=1'
PROXIES = {
    'HTTP': '91.144.140.125:8080',
    'HTTPS': '77.50.104.110:3128'
}
HEADERS = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
}

orders = []
log = logging.getLogger("parser")

def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler("parser.log")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)

def start_parsing():
    response = requests.get(URL, headers=HEADERS)
    html_text = response.text
    log.info(f'STATUS CODE - {response.status_code}')

    soup = bsoup(html_text, 'html.parser')
    order_data = soup.find_all('div', class_='search-item-body')
    orders.extend(order_data)

    for i in range(0, 5):
        info_order = orders[i]
        title = info_order.find('a').text
        price = info_order.find('span', class_='search-price')

        if price != None:
            price = price.text
        else:
            price = "Договорная"

        print(title, price)



if __name__ == '__main__':
    configure_logging()
    start_parsing()
