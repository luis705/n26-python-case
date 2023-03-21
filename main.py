import string
from hashlib import md5
from random import choice

import pandas as pd
import requests

from keys import Keys


def generate_ts(quantity: int = 10) -> str:
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for _ in range(quantity))


def md5_checksum(pub_key: str, priv_key: str, ts: str) -> str:
    encoded = (ts + priv_key + pub_key).encode('utf-8')
    return md5(encoded).hexdigest()


def get_character_data(character_json: dict) -> list:
    character_data = [
        character_json.get(value) for value in ['id', 'name', 'description']
    ]
    quantity_data = [
        character_json.get(value).get('available')
        for value in ['comics', 'series', 'stories', 'events']
    ]
    return character_data + quantity_data


def api_call(
    offset: int = 0,
    missing: int = 0,
    pub_key: str = Keys.pub_key,
    priv_key: str = Keys.priv_key,
) -> tuple[int, dict]:
    # API url
    base_url = 'https://gateway.marvel.com:443/'
    endpoint = '/v1/public/characters?'
    url = base_url + endpoint

    # Auth
    ts = generate_ts()
    auth_hash = md5_checksum(pub_key, priv_key, ts)

    # Request
    param = {
        'ts': ts,
        'apikey': pub_key,
        'hash': auth_hash,
        'limit': missing,
        'offset': offset,
        'orderBy': 'name',
    }
    response = requests.get(url, params=param).json().get('data')
    return response.get('total'), response.get('results')


def main():
    offset = 0
    result = []
    missing = 100

    while True:
        total, response = api_call(offset, missing)
        for character in response:
            result.append(get_character_data(character))
        offset += missing

        # Checks if there are still more data to fetch
        missing = min(total - offset, 100)
        if missing <= 0:
            break

    # Creates and saves dataframe to disk
    df = pd.DataFrame(
        result,
        columns=[
            'id',
            'name',
            'description',
            'comics',
            'series',
            'stories',
            'events',
        ],
    )
    df.to_csv('Case python - result.csv')


if __name__ == '__main__':
    main()
