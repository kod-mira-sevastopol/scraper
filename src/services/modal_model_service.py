from datetime import datetime
import src.helpers.presets as presets
from src.async_modal.main import getAnswer


class ModalModelService:
    @staticmethod
    async def modal_scrab(resume_text):
        get_modal_scrab_url = 'https://enotgpt-gai-server.serveo.net/sendTextMessage?message='
        timer = datetime.now()

        action = presets.Presets.get_preset('action')
        format = presets.Presets.get_preset('format')

        message = f'{resume_text} {action} {format}'

        blackwords = presets.Presets.get_banwords()

        for word in blackwords:
            message = message.replace(word, ' ')

        '''
        body = {
            'message': message.lower(),
            'temperature': 0.87
        }
        '''

        body = [
            {
                "role": "user",
                "content": message
            }
        ]

        print(message)

        response = await getAnswer(body)
        # response = requests.post(url=get_modal_scrab_url, json=body).json()

        print(datetime.now() - timer)
        print(response)
        return response

