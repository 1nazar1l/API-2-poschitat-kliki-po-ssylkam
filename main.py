import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import argparse


def shorten_link(headers, long_url):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    params = {
        "long_url": long_url
    }
    response = requests.post(url, json=params, headers=headers)
    response.raise_for_status() 
    return response.json()['link']


def count_clicks(headers, bitlink):
    bitlink = urlparse(bitlink)
    bitlink = f'{bitlink.netloc}{bitlink.path}'
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    total_clicks = response.json()['total_clicks']
    return total_clicks


def is_bitlink(headers, url):
    bitlink = urlparse(url)
    bitlink = f'{bitlink.netloc}{bitlink.path}'
    link = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(link, headers=headers)
    return response.ok


def main():
    load_dotenv()
    secret = os.getenv("BITLY_TOKEN")
    header = {
        "Authorization": f"Bearer {secret}"
    }
    parser = argparse.ArgumentParser(description='Сокращает ссылку или пишет количество переходов по ней.')
    parser.add_argument('url', help='Ссылка на сайт: ')
    args = parser.parse_args()
    try:
        if is_bitlink(header, args.url):
            print('Кол-во кликов', count_clicks(header, args.url))
        else:
            print('Битлинк:', shorten_link(header, args.url))
    except requests.exceptions.HTTPError:
        print("Ссылка введена неправильно.")
           
if __name__ == "__main__":
    main()
