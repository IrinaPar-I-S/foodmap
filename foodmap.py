import telebot
import requests
import json
import conf
import emoji
from bs4 import BeautifulSoup
from dadata import Dadata
from math import radians, cos, sin, asin, sqrt



bot = telebot.TeleBot(conf.TOKEN)

prms = {'district[]':'','metro[]':[],'cuisine[]':'','bill[]':[]}
flag = ['']
names = {}
my_lat,my_lon = [''],['']




#здесь хранятся кнопки для пользователя
def menu () :
    me_nu = telebot.types.InlineKeyboardMarkup()
    me_nu.add(telebot.types.InlineKeyboardButton(text='Адрес',callback_data='/address'))
    me_nu.add(telebot.types.InlineKeyboardButton(text='Метро',callback_data='/metro'))
    me_nu.add(telebot.types.InlineKeyboardButton(text='Кухня',callback_data='/cuisine'))
    me_nu.add(telebot.types.InlineKeyboardButton(text='Цена',callback_data='/price'))
    me_nu.add(telebot.types.InlineKeyboardButton(text='Поиск',callback_data='/search'))
    me_nu.add(telebot.types.InlineKeyboardButton(text='Сбросить введенные данные',callback_data='/cancel'))
    me_nu.add(telebot.types.InlineKeyboardButton(text='Помощь',callback_data='/help'))
    return me_nu




#алгоритм Хаверсина, для вычисления расстояния
def haversine (lat1,lon1,lat2,lon2):
    lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2)) #перевод в радианы
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    km = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    km = 2*asin(sqrt(km))
    km = 6367*km
    return km




#это хэндлер сообщений с меню
@bot.callback_query_handler(func=None)
def defining_buttons(message):
    if message.data == '/start' :
        starting(message)
    elif message.data == '/address' :
        getting_address(message)
    elif message.data == '/metro' :
        getting_metro(message)
    elif message.data == '/cuisine' :
        getting_cuisine(message)
    elif message.data == '/price' :
        getting_price (message)
    elif message.data == '/cancel' :
        cancelling(message)
    elif message.data == '/help' :
        helping(message)
    elif message.data == '/search' :
        searching(message)
    elif message.data == '/nearest' :
        nearest(message)
    else :
        prms['cuisine[]'] = message.data
        print(prms)
        bot.send_message(message.from_user.id,emoji.emojize(':ok_hand:',use_aliases=True),reply_markup=menu())




#просто начальное сообщение, не знаю даже, зачем оно нужно
@bot.message_handler(commands=['start'])
def starting (message) :
    flag[0] = '0'
    prms['district[]'],prms['metro[]'],prms['cuisine[]'],prms['bill[]'] = '',[],'',[]
    item = telebot.types.InlineKeyboardButton(text='Ссылка на сайт',url='msk.allcafe.ru')
    allcafe = telebot.types.InlineKeyboardMarkup().add(item)
    item = menu()
    bot.send_message(message.from_user.id,'Добро пожаловать! Я бот, подбирающий список ресторанов, кафе и баров с сайта allcafe.ru',reply_markup=allcafe)
    bot.send_message(message.from_user.id,'Какие параметры ты хочешь учесть при выборе?',reply_markup=item)




# ??? доработать, чтоб можно было выбрать несколько ???
#просто меню с выбором кухни
@bot.message_handler(commands=['cuisine'])
def getting_cuisine (message) :
    Cuisine = telebot.types.InlineKeyboardMarkup()
    Cuisine.add(telebot.types.InlineKeyboardButton(text='авторская',callback_data='avtorskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='азиатская',callback_data='aziatskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='американская',callback_data='amerikanskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='вегетарианская',callback_data='vegetarianskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='восточная',callback_data='vostochnaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='грузинская',callback_data='gruzinskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='еврейская',callback_data='evreyskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='европейская',callback_data='evropeyskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='итальянская',callback_data='italyanskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='кавказская',callback_data='kavkazskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='китайская',callback_data='kitayskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='корейская',callback_data='koreyskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='немецкая',callback_data='nemetskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='паназиатская',callback_data='panaziatskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='русская',callback_data='russkaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='смешанная',callback_data='smeshannaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='средиземноморская',callback_data='sredizemnomorskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='узбекская',callback_data='uzbekskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='французская',callback_data='frantsuzskaya'))
    Cuisine.add(telebot.types.InlineKeyboardButton(text='японская',callback_data='yaponskaya'))
    bot.send_message(message.from_user.id,'Выбери любимую кухню:',reply_markup=Cuisine)
    



#штука сравнивает численные значения из данных и написанное пользователем
@bot.message_handler(commands=['price'])
def getting_price (message) :
    flag[0] = '1' #отсылка к нужной функции
    bot.send_message(message.from_user.id,'Какую максимальную сумму в рублях ты готов заплатить? Введи цифру')
        



#штука обращается к json-у и берет оттуда станцию метро по названию
@bot.message_handler(commands=['metro'])
def getting_metro (message) :
    flag[0] = '2' #отсылка к нужной функции
    bot.send_message(message.from_user.id,'Введи название станции')
    
        

#штука использует Dadata и достает район и станцию метро
@bot.message_handler(commands=['address'])
def getting_address (message) :
    flag[0] = '3' #отсылка к нужной функции
    bot.send_message(message.from_user.id,'Введи адрес: улицу (по возможности, номер дома)')

    


#просто сообщение с инструкцией
@bot.message_handler(commands=['help'])
def helping (message) :
    prms['district[]'],prms['metro[]'],prms['cuisine[]'],prms['bill[]'] = '',[],'',[]
    item = menu()
    bot.send_message(message.from_user.id,'Бот помогает находить рестораны, кафе, бары, закусочные, используя несколько параметров, с помощью сайта allcafe.ru\n\nДля того, чтобы воспользоваться ботом, введи /start\nДля того, чтобы сбросить данные, введенные ранее, введи /cancel\n\nКоманда /address позволяет искать места поблизости, ту же функцию выполняет команда /metro, поэтому можно выбрать одну из них. Если потом из списка мест будет интересно посмотреть ближайшие - обязательно указывать адрес. Команда /price позволяет ограничить предполагаемую сумму чека.\nПри использовании каждой из этих команд бот предложит ввести соответственно адрес, название станции метро или сумму с помощью клавиатуры.\nКоманда /cuisine позволяет выбрать кухню.\n\nЗапрос после введения всех данных отправляется с помощью команды /search.\nПосле выдачи результатов чтобы узнать, какие пять мест ближе всего к тебе, введи команду /nearest\n\nПриятного пользования!')




#чистилка параметров
@bot.message_handler(commands=['cancel'])
def cancelling (message) :
    prms['district[]'],prms['metro[]'],prms['cuisine[]'],prms['bill[]'] = '',[],'',[]
    bot.send_message(message.from_user.id,'Данные запросов очищены '+emoji.emojize(':ok_hand: \n Можно начинать заново \n\n',use_aliases=True),reply_markup=menu())




#команда поиска
@bot.message_handler(commands=['search'])
def searching (message) :
    addresses, links = [],[]
    req='https://msk.allcafe.ru/catalog/?query='
    html = requests.get(req, params = prms) #запрос на сайт
    req = html.request.url
    print (req)
    html = html.text
    soup = BeautifulSoup(html,'html.parser')
    for name in soup.find_all('a', {'class':'placeList_name'}) : #ищет названия мест
        a = name.text.strip()
        def like_counter(a) : #эта сложная штука нужна, чтобы повторяющиеся названия включились в словарь
            if not a in names.keys() :
                names[a] = ''
            else :
                a += ' '
                like_counter(a)
        like_counter(a)
        b = str(name) #там в тэге ссылка
        b = b.split('"')
        b = b[3]
        links.append(b)
    if len(links) == 0 :
        item = telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Начать заново',callback_data='/start'))
        bot.send_message(message.from_user.id,emoji.emojize('Ничего не удалось найти :cry: \n\n',use_aliases=True),reply_markup=item)
    else :
        for i in range (len(soup.find_all('span', {'class':'placeList_addr'}))) : #ищет адреса мест в том же порядке
            addr = soup.find_all('span', {'class':'placeList_addr'})[i]
            a = addr.text.strip()
            a = a.replace('\n','')
            a = a.replace('  ','')
            addresses.append(a)
        n=0 #счетчик
        for i in names.keys() :
            names[i] = addresses[n] #добавляет адрес к названию
            n+=1 #счетчик
        bot.send_message(message.from_user.id,'Вот что мне удалось найти:')
        out=' '
        n=0 #счетчик
        for k, v in names.items() :
            out += k+'\n'+v+'\nmsk.allcafe.ru'+links[n]+'\n\n'
            if n%10 == 0 :
                bot.send_message(message.from_user.id,out)
                out = ' '
            n+=1 #счетчик
        item = telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Начать заново',callback_data='/start'))
        bot.send_message(message.from_user.id,out,reply_markup=item)
        item = telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Ссылка на поисковый запрос',url=req))
        bot.send_message(message.from_user.id,'\n',reply_markup=item)
        item = telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Найти ближайшие',callback_data='/nearest'))
        bot.send_message(message.from_user.id,'Чтобы узнать, какие пять мест ближе всего к тебе, введи команду /nearest (только если до этого ты указывал свой адрес)',reply_markup=item)




#функция поиска ближайших мест
@bot.message_handler(commands=['nearest'])
def nearest (message) :
    near_me = {}
    for k, v in names.items() :
        dadata = Dadata(conf.a,conf.b)
        address = dadata.clean('address',v)
        lat,lon = float(address['geo_lat']),float(address['geo_lon'])
        a = haversine(lat,lon,my_lat[0],my_lon[0])
        near_me[k] = a
    out,n = '',1
    item = telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Начать заново',callback_data='/start'))
    for i in sorted(near_me.keys(), key=lambda x: near_me[x]) :
        out += i+'\n'+names[i]+'\n\n'
        if n == 5 :
            bot.send_message(message.from_user.id,out,reply_markup=item)
            break
        else :
            n+=1 #счетчик





#все сложно с текстовыми сообщениями, поэтому тут одна функция, которая на самом деле разная
@bot.message_handler(content_types=['text'])
def getting_text_messages (message,flag=flag) :
    if flag[0] == '0' : #дефолтный вариант
        item = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True).row('/help')
        bot.send_message(message.chat.id,'Не понимаю, что ты хочешь сказать. Попробуй воспользоваться кнопкой /help',reply_markup=item)
    elif flag[0] == '1' : #для функции определения цены
        price = message.text
        with open ('price.json', 'r', encoding='utf-8') as f :
            Price = json.load(f)
        for k in Price.keys() :
            if int(k) <= int(price) :
                prms['bill[]'].append (Price[k])
        print(prms)
        bot.send_message(message.from_user.id,emoji.emojize(':ok_hand: \n\n',use_aliases=True),reply_markup=menu())
        flag = 0
    elif flag[0] == '2' : #для функции определения метро
        metro = message.text
        with open ('metro.json', 'r', encoding='utf-8') as f :
            Metro = json.load(f)
        prms['metro[]'] = Metro.get(metro.lower(),'') #чтоб если чего-то нет в списке, он не сломался
        print(prms)
        if prms['metro[]'] == '' :
            bot.send_message(message.from_user.id,emoji.emojize('Такого не нашлось :cry: \n\n',use_aliases=True),reply_markup=menu())
            flag = 0
        else :
            bot.send_message(message.from_user.id,emoji.emojize(':ok_hand: \n\n',use_aliases=True),reply_markup=menu())
            flag = 0
    elif flag[0] == '3' : #для функции определения адреса
        address = 'Москва '+message.text
        with open ('metro.json', 'r', encoding='utf-8') as f :
            Metro = json.load(f)
        with open ('districts.json', 'r', encoding='utf-8') as f :
            Districts = json.load(f)
        dadata = Dadata(conf.a,conf.b)
        address = dadata.clean('address', address)
        print (address)
        if address['city_district'] != None : #чтоб если адрес неправильный, он не сломался
            my_lat[0],my_lon[0] = float(address['geo_lat']),float(address['geo_lon'])
            district = address['city_district'].strip().lower()
            if isinstance(address['metro'],list) : #может быть несколько станций метро или одна
                for i in address['metro'] :
                    prms['metro[]'].append(Metro.get(i['name'].strip().lower(),'арбатская')) #чтоб если чего-то нет в списке, он не сломался
            else :
                prms['metro[]'] = Metro.get(address['metro'],'арбатская')
            prms['district[]'] = Districts.get(district,'арбат') #чтоб если чего-то нет в списке, он не сломался
            print(prms)
            bot.send_message(message.from_user.id,emoji.emojize(':ok_hand: \n\n',use_aliases=True),reply_markup=menu())
        else :
            bot.send_message(message.from_user.id,emoji.emojize('Адрес ошибочный :cry: \n\n',use_aliases=True),reply_markup=menu())
        flag = 0
        


if __name__ == '__main__':
    bot.polling(none_stop=True)
