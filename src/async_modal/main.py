import ssl
import aiohttp

from src.async_modal.auth import get_token


async def getAnswer(messages: list[dict], temperature: float = 0.8) -> dict:
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
    access_token = await get_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "model": "GigaChat:latest",
        "messages": messages,
        "temperature": temperature
    }

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.post(url, headers=headers, json=data) as response:
            result = await response.json()

    return result