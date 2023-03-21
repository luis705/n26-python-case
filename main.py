import json
import random
import string
from hashlib import md5

import pandas as pd
import requests

from keys import Keys


def generate_ts():
    letras = string.ascii_lowercase
    return ''.join(random.choice(letras) for i in range(25))


def md5_checksum(pub_key, priv_key, ts):
    codificada = (ts + priv_key + pub_key).encode('utf-8')
    return md5(codificada).hexdigest()


def get_character_data(character_json):
    metadata = 'id', 'name', 'description'
    data = 'comics', 'series', 'stories', 'events'
    character_data = [character_json.get(value) for value in metadata]
    for value in data:
        character_data.append(character_json.get(value).get('available'))
    return character_data


def api_call(offset=0, missing=0,  pub_key=Keys.pub_key, priv_key=Keys.priv_key):
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
        'orderBy': 'name'
    }
    response = requests.get(url, params=param).json().get('data')
    return response.get('total'), response.get('results')


def main():
    offset = 0
    result = []
    missing = 100
    # Checks if all the data has been received
    while True:
        total, response = api_call(offset, missing)
        for character in response:
            result.append(get_character_data(character))
        offset += missing

        # Checks if requests are done
        missing = min(total - offset, 100)
        print(total, offset, missing)
        if missing <= 0:
            break

    df = pd.DataFrame(result, columns=['id', 'name', 'description', 'comics', 'series', 'stories', 'events'])
    df.to_csv('Case python - result.csv')


if __name__ == '__main__':
    main()
