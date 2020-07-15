import re
import requests
import json

URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'


# Загрузка курсов валют по URL-адресу
# Возвращение данных в формате словаря(dict).


def load_exchange():
    return json.loads(requests.get(URL).text)


# Возвращение курса по запрошенной валюте

def get_exchange(ccy_key):
    for exc in load_exchange():
        if ccy_key == exc['ccy']:
            return exc
    return False


# возвращает список валют в соответствии с шаблоном

def get_exchanges(ccy_pattern):
    result = []
    ccy_pattern = re.escape(ccy_pattern) + '.*'
    for exc in load_exchange():
        if re.match(ccy_pattern, exc['ccy'], re.IGNORECASE) is not None:
            result.append(exc)
    return result
