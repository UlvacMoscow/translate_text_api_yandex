from pprint import pprint

import requests
import os


translate_text = 'translate_text'
practice_file = os.path.dirname(os.path.abspath(__file__))
print(practice_file)
text_dir = os.listdir(practice_file)
list_text = []
dict_text_and_path = {}

for text in text_dir:
    if text.endswith('.txt'):
        list_text.append(text)

for text in list_text:
    path = os.path.join(practice_file,text)
    dict_text_and_path.update({text : path})

# pprint(list_text)
pprint(dict_text_and_path)


def detected(text):

    with open(text,'rb') as f:
        data = f.read()
        # print(data)
    url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    key = 'trnsl.1.1.20180314T183313Z.c599ef041df6e543.0aed557ca792f3a154b8567042b0ee0065153a50'

    params = {
        'key' : key,
        'text' : data,
        'hint': ['de','es','fr']
    }
    response = requests.get(url, params=params).json()
    # print(response)
    return ''.join(response.get('lang', []))


def translate_it(text,lang):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """

    with open(text,'rb') as f:
        data = f.read()
        # print(data)
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    params = {
        'key': key,
        'lang': '{}-ru'.format(lang),
        'text': data,
    }
    response = requests.get(url, params=params).json()
    # print(response)
    return ' '.join(response.get('text', []))

for text in dict_text_and_path:
    # print(text,dict_text_and_path[text])
    lang = detected(dict_text_and_path[text])
    result = translate_it(dict_text_and_path[text],lang)
    folder_result_way = os.path.join(practice_file, translate_text)

    if not os.path.exists(folder_result_way):
        os.mkdir(folder_result_way)
    path = os.path.join(practice_file, folder_result_way,'{}.txt'.format(lang))
    my_file = open(path, 'w')
    my_file.write(result)
    my_file.close()
    print(lang,result)