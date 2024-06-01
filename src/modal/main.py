import os
from json import loads

import requests

from src.modal.auth import getToken

keys = [
    {
        'name': 'kostya',
        'secret': os.getenv("kostya_secret"),
        'client': os.getenv("kostya_client"),
        'auth': os.getenv('kostya_auth'),
    },
    {
        'name': 'daniil',
        'secret': '',
        'client': '',
        'auth': '',
    },
    {
        'name': 'misha',
        'secret': '',
        'client': '',
        'auth': '',
    },
]


def getAnswer(messages: list[dict], temperature: float = 0.87) -> dict:
    """
    messages": [
            {
                "role": "user",
                "content": "Когда уже ИИ захватит этот мир?"
            },
            {
                "role": "assistant",
                "content": "Пока что это не является неизбежным событием. Несмотря на то, что искусственный интеллект (ИИ) развивается быстрыми темпами и может выполнять сложные задачи все более эффективно, он по-прежнему ограничен в своих возможностях и не может заменить полностью человека во многих областях. Кроме того, существуют этические и правовые вопросы, связанные с использованием ИИ, которые необходимо учитывать при его разработке и внедрении."
            },
            {
                "role": "user",
                "content": "Думаешь, у нас еще есть шанс?"
            }
        ],

        temperature = number <float> [ 0 .. 2 ]
        По умолчанию: 0.87
        Температура выборки в диапазоне от ноля до двух. Чем выше значение, тем более случайным будет ответ модели.
    """

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {getToken()}"
    }

    data = {
        "model": "GigaChat:latest",
        "messages": messages,
        "temperature": temperature
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    result = loads(response.text)
    return result
