import requests
from bs4 import BeautifulSoup
from dadata import Dadata
import json

address = 'Москва ' + input('Введите ваше местоположение... ')
price = input('Максимальная сумма чека... ')

#тут, я думаю, можно, чтоб вводить все параметры, а можно иногда "пропуск"
#и надо еще про кухню спросить не забыть (это я себе)

#ниже я все переменные указываю, чтоб не запутаться

names, addresses, metro = [],[],[]
req = 'https://msk.allcafe.ru/catalog/?query='


if address != 'пропуск' :
    dadata = Dadata('42e5e62148b540bbf9662f1ac4076443d64fa6b9','37b7e6a312147176befc5af1e3be6c783a5ec797')
#(это я себе) выдача идет в формате:
#city_district Басманный
#metro [{'distance': 0.9, 'line': 'Сокольническая', 'name': 'Комсомольская'}, {'distance': 0.9, 'line': 'Сокольническая', 'name': 'Красные ворота'}]
    address = dadata.clean('address', address)
    district = address['city_district'].strip().lowercase()
    for i in address['metro'] :
        metro.append (i['name'].strip().lowercase())
    req += '&district[]='+dic_Districts.get(district,'арбат') #чтоб если чего-то нет в списке, он не сломался
    for i in range (len(metro)) :
        req += '&metro[]='+dic_Metro.get(metro[i],'арбатская') #чтоб если чего-то нет в списке, он не сломался

if price != 'пропуск' :
    price = int(price)
    for k in dic_Price.keys() :
        if k <= price :
            req += '&bill[]='+dic_Price[k]

#(это я опять себе) адресную строку задавать в порядке district - metro - cuisine - bill

html = requests.get(req).text
soup = BeautifulSoup(html,'html.parser')
for name in soup.find_all('a', {'class':'placeList_name'}) :
    a = name.text.strip()
    if a in names :
        pass
    else :
        names.append (a)
#тут надо доработать, потому что такая тема будет раблотать, если все разные метса с разными адресами,
#а если в одном доме несколько или, например, сеть с несколькими точками - все развалится
for addr in soup.find_all('span', {'class':'placeList_addr'}) :
    a = addr.text.strip()
    if a in addresses :
        pass
    else :
        while '\n' in a :
            a = a.replace('\n','')
        addresses.append (a)
for i in range (len (names)) :
    print(names[i], '\n', addresses[i])
#ну, а вообще, он пока что выводит список, и я не знаю, что делать дальше
