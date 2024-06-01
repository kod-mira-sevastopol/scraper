import os
from json import loads

import requests
from dotenv import load_dotenv

load_dotenv()

#print(os.getenv('client_id_1'))
tokens = [
    {
        "client_secret": os.getenv('client_secret_1'),
        "client_id": os.getenv('client_id_1'),
        "auth_data": os.getenv('auth_data_1'),
        "scope": "GIGACHAT_API_PERS",
        "token": ""
    },
    {
        "client_secret": os.getenv('client_secret_2'),
        "client_id": os.getenv('client_id_2'),
        "auth_data": os.getenv('auth_data_2'),
        "scope": "GIGACHAT_API_PERS",
        "token": ""
    },
    {
        "client_secret": os.getenv('client_secret_3'),
        "client_id": os.getenv('client_id_3'),
        "auth_data": os.getenv('auth_data_3'),
        "scope": "GIGACHAT_API_PERS",
        "token": ""
    }
]


async def move_token_to_front(token: str):
    for i, t in enumerate(tokens):
        if t["token"] == token:
            obj = tokens.pop(i)
            tokens.insert(0, obj)
            return True


async def auth_token_request():
    """"
        Отправить запрос на получение токена
    """
    url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    auth_data = tokens[0]['auth_data']
    print(auth_data)
    client_secret = tokens[0]['client_secret']
    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': client_secret,
        'Authorization': f'Basic {auth_data}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    response = loads(response.text)
    tokens[0]['token'] = response['access_token']
    first_element = tokens.pop(0)
    tokens.append(first_element)
    return response


async def get_token():
    res = await auth_token_request()
    return res['access_token']
