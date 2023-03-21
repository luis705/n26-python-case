import random
import string
from hashlib import md5
import json

import requests

from keys import Keys


def generate_ts():
    letras = string.ascii_lowercase
    return ''.join(random.choice(letras) for i in range(25))


def md5_checksum(pub_key, priv_key, ts):
    codificada = (ts + priv_key + pub_key).encode('utf-8')
    return md5(codificada).hexdigest()


# API url
base_url = 'https://gateway.marvel.com:443/'
endpoint = '/v1/public/characters?'
url = base_url + endpoint

# Auth
ts = generate_ts()
auth_hash = md5_checksum(Keys.pub_key, Keys.priv_key, ts)

# Request
param = {'ts': ts, 'apikey': Keys.pub_key, 'hash': auth_hash, 'limit': 1}
r = requests.get(url, params=param)

dados = r.json().get('data').get('results')

with open("sample_data.json", mode='w') as outfile:
    json.dump(dados[0], outfile)


