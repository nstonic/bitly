import requests
import os
from dotenv import load_dotenv
import argparse
from urllib.parse import urlparse


def get_short_link(long_link: str, token: str) -> str:
    headers = {
        'Authorization': f'Bearer {token}',
    }

    long_url = {
        "long_url": long_link
    }

    url = 'https://api-ssl.bitly.com/v4/shorten'

    short_link_response = requests.post(url=url, headers=headers, json=long_url)
    short_link_response.raise_for_status()

    return short_link_response.json()['link']


def count_clicks(bitly_link: str, token: str) -> int:
    headers = {
        'Authorization': f'Bearer {token}',
    }

    params = (
        ('unit', 'month'),
        ('units', '-1'),
    )

    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitly_link}/clicks/summary'

    counter_response = requests.get(url=url, headers=headers, params=params)
    counter_response.raise_for_status()

    return counter_response.json()['total_clicks']


def is_bitlink(input_link: str, token: str) -> bool:
    headers = {
        'Authorization': f'Bearer {token}',
    }

    url = f"https://api-ssl.bitly.com/v4/bitlinks/{input_link}"

    bitly_response = requests.get(url=url, headers=headers)
    return bitly_response.ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_link")
    args = parser.parse_args()
    input_link = args.input_link
    parsed_link = urlparse(input_link)
    link_without_scheme = ''.join(parsed_link[1:])
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']

    if is_bitlink(link_without_scheme, bitly_token):
        click_counter = count_clicks(link_without_scheme, bitly_token)
        print(f"По Вашей ссылке прошли {click_counter} раз(а)")
    else:
        print("Битлинк: ", get_short_link(input_link, bitly_token))


if __name__ == "__main__":
    main()
