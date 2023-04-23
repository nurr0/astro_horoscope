import requests
import json
from fastapi.responses import JSONResponse
def get_horoscope(sign):
    response = requests.get(f'http://horoscopes.rambler.ru/api/front/v3/horoscope/love/{sign}/today/').text
    result = {'data': json.loads(response)['content']['text'][0]['content']}
    return result

def get_full_horoscope(sign):
    response = requests.get(f'http://horoscopes.rambler.ru/api/front/v3/horoscope/love/{sign}/today/').json()
    return response


def get_name_meaning(name):
    try:
        with open('name_dict1.json', 'r', encoding='cp1251') as f:
            data = json.load(f)
            name_info = data[name]
    except:
        try:
            with open('name_dict2.json', 'r', encoding='cp1251') as f:
                data = json.load(f)
                name_info = data[name]
        except:
            name_info = JSONResponse(content={"detail": "Not found"}, status_code=404)
    return name_info
