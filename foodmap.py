import requests
from bs4 import BeautifulSoup
from dadata import Dadata
import json


prms = {'district[]':'','metro[]':[],'cuisine[]':'','bill[]':[]}
 

def defining_address (prms) :
    address = 'Москва ' + input('Введите ваше местоположение... ')
    if address != 'пропуск' :
        with open ('metro.json', 'r', encoding='utf-8') as f :
            Metro = json.load(f)
        with open ('districts.json', 'r', encoding='utf-8') as f :
            Districts = json.load(f)
        Districts = json.load(f)
        dadata = Dadata('42e5e62148b540bbf9662f1ac4076443d64fa6b9','37b7e6a312147176befc5af1e3be6c783a5ec797')
#(это я себе) выдача идет в формате:
#city_district Басманный
#metro [{'distance': 0.9, 'line': 'Сокольническая', 'name': 'Комсомольская'}, {'distance': 0.9, 'line': 'Сокольническая', 'name': 'Красные ворота'}]
        address = dadata.clean('address', address)
        district = address['city_district'].strip().lowercase()
        if isinstance(address['metro'],list) :
            for i in address['metro'] :
                prms['metro[]'].append (Metro.get(i['name'].strip().lowercase(),'арбатская'))
        else :
            prms['metro[]'] = Metro.get(address['metro'],'арбатская')
        prms['district[]'] = Districts.get(district,'арбат') #чтоб если чего-то нет в списке, он не сломался
    return prms



def defining_cuisine (prms) :
    cuisine = input('Предпочитаемая кухня...')
    if cuisine != 'пропуск' :
        with open ('cuisine.json', 'r', encoding='utf-8') as f :
            Cuisine = json.load(f)
        prms['cuisine[]'] = Cuisine.get(cuisine,'европейская')
    return prms



def defining_price (prms) :
    price = int(input('Максимальная сумма чека... '))
    if price != 'пропуск' :
        price = int(price)
        for k in Price.keys() :
            if k <= price :
                prms['bill[]'].append (Price[k])
    return prms



#тут надо доработать
def getting_places (prms) :
    req='https://msk.allcafe.ru/catalog/?query='
    names, addresses = [],[]
    html = requests.get(req, params = prms).text #запрос на сайт
    soup = BeautifulSoup(html,'html.parser')
    for name in soup.find_all('a', {'class':'placeList_name'}) : #ищет названия мест
        a = name.text.strip()
        if not a in names :
            names.append (a)
    for addr in soup.find_all('span', {'class':'placeList_addr'}) : #ищет адреса мест в том же порядке
        a = addr.text.strip()
        if not a in addresses :
            a = a.replace('\n','')
            addresses.append (a)
    return names, addresses

#ну, а вообще, я не знаю, что делать дальше
