import requests
import json

def get_horoscope(sign):
    response = requests.get(f'http://horoscopes.rambler.ru/api/front/v3/horoscope/love/{sign}/today/').text
    result = {'data': json.loads(response)['content']['text'][0]['content']}
    return result

def get_full_horoscope(sign):
    response = requests.get(f'http://horoscopes.rambler.ru/api/front/v3/horoscope/love/{sign}/today/').json()
    return response
