import random

import requests
from bs4 import BeautifulSoup as bsoup
from prettytable import PrettyTable
import time
import logging

KEYWORD = 'php'
PAGE_COUNT = 2
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

def prepare_url(word='python', page=1):
    url = f'https://www.fl.ru/search/?type=projects&action=search&search_string={str(word).lower()}&search_hint=Next%2Bgen&page={page}'
    return url

def print_result(table):
    th = ["NAME", "PRICE"]
    td = table
    columns = len(th)
    ptable = PrettyTable(th)
    td_data = td[:]

    while td_data:
        ptable.add_row(td_data[:columns])
        td_data = td_data[columns:]

    print(ptable)

def delay():
    value = random.random()
    scaled_value = 1 + (value * (9 - 5))
    log.info(f"DELAY - {scaled_value} SEC.")
    time.sleep(scaled_value)

def start_parsing():
    for i in range(1, PAGE_COUNT):
        url = prepare_url(word=KEYWORD, page=i)
        response = requests.get(url, headers=HEADERS)
        html_text = response.text
        log.info(f'STATUS CODE - {response.status_code}')
        soup = bsoup(html_text, 'html.parser')
        order_data = soup.find_all('div', class_='search-item-body')

        if order_data != []:
            orders.extend(order_data)
            #   Задержка для парсера
            delay()
        else:
            log.info("EMPTY")
            break

    result = []

    for i in range(len(orders)):
        info_order = orders[i]
        title = info_order.find('a').text
        price = info_order.find('span', class_='search-price')

        if price != None:
            price = price.text
        else:
            price = "Договорная"

        result.extend([title])
        result.extend([price])

    print_result(result)

if __name__ == '__main__':
    configure_logging()
    start_parsing()
