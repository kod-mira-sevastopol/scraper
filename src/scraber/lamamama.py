from llamaapi import LlamaAPI
import json
from docx2txt import docx2txt

llama = LlamaAPI('LL-S15dvHuM9LiEKkB6lIoBPoOM0FTTenJTo40ONUi8Ud1D1xqVHyqxr87sIM24aROo')

api_request_json = {
    "messages": [
        {"role": "user", "content": ""},
    ],
    "functions": [
        {'name': 'get_resume',
         'description': 'Extracts the relevant information from the resume.',
         'parameters': {
             'type': 'object',
             'properties': {
                 'fcs': {
                     'title': 'FCS',
                     'type': 'string',
                     'description': 'the first_name, the second_name or maybe last_name'
                 },
                 'stack': {
                     'title': 'stack_list',
                     'type': 'object',
                     'properties': {
                         'item': {
                             'title': 'stac_item',
                             'type': 'string',
                             'description': 'the technology he uses'
                         },
                     }
                 },
             },
             'required': ['fcs', 'stack']
         }
         }
    ],
    "stream": False,
    "function_call": {"name": "get_resume"},
}


def scrap_file(path):
    text = docx2txt.process(path)
    return text


# Make your request and handle the response
text = scrap_file('tests/docx.docx')
api_request_json['messages'][0]['context'] = f'Extract the desired information from the following resume.:\n\n{text}'
print(api_request_json)
response = llama.run(api_request_json)
print(json.dumps(response.json(), indent=2))
