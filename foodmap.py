import telebot
import requests
import json
import conf
import emoji
from bs4 import BeautifulSoup
from dadata import Dadata



bot = telebot.TeleBot(conf.TOKEN)

prms = {'district[]':'','metro[]':[],'cuisine[]':'','bill[]':[]}
flag = ['']



#здесь хранятся кнопки для пользователя
def menu () :
    me_nu = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    me_nu.row('/address', '/metro')
    me_nu.row('/cuisine', '/price')
    me_nu.row('/search')
    me_nu.row('/start', '/help', '/cancel')
    return me_nu



#просто начальное сообщение, не знаю даже, зачем оно нужно
@bot.message_handler(commands=['start'])
def starting (message) :
    flag[0] = '0'
    item = telebot.types.InlineKeyboardButton(text='Ссылка на сайт',url='msk.allcafe.ru')
    allcafe = telebot.types.InlineKeyboardMarkup().add(item)
    item = menu()
    bot.send_message(message.chat.id,'Добро пожаловать! Я бот, подбирающий список ресторанов, кафе и баров с сайта allcafe.ru',reply_markup=allcafe)
    bot.send_message(message.chat.id,'Какие параметры ты хочешь учесть при выборе?',reply_markup=item)



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
    @bot.callback_query_handler(func=None)
    def defining_cuisine(message):
        prms['cuisine[]'] = message.data
        print(prms)
        bot.send_message(message.from_user.id,emoji.emojize(':ok_hand:',use_aliases=True),reply_markup=menu())
        


#штука сравнивает численные значения из данных и написанное пользователем
@bot.message_handler(commands=['price'])
def getting_price (message) :
    flag[0] = '1' #отсылка к нужной функции
    bot.send_message(message.from_user.id,'Какую максимальную сумму в рублях ты готов заплатить? Введи цифру')
        



# ??? доработать, чтоб можно было выбрать несколько ???
#штука обращается к json-у и берет оттуда станцию метро по названию
@bot.message_handler(commands=['metro'])
def getting_metro (message) :
    flag[0] = '2' #отсылка к нужной функции
    bot.send_message(message.from_user.id,'Введи название станции')
    
        

#штука использует Dadata и достает район и станцию метро
@bot.message_handler(commands=['address'])
def getting_address (message) :
    flag[0] = '3' #отсылка к нужной функции
    bot.send_message(message.from_user.id,'Введи название станции')

    


#просто сообщение с инструкцией
@bot.message_handler(commands=['help'])
def helping (message) :
    item = menu()
    bot.send_message(message.from_user.id,'Бот помогает находить рестораны, кафе, бары, закусочные, используя несколько параметров, с помощью сайта allcafe.ru\n\nДля того, чтобы воспользоваться ботом, нажми start\nДля того, чтобы сбросить данные, введенные ранее, нажми cancel\n\nКоманда address позволяет искать места поблизости, ту же функцию выполняет команда metro, поэтому их лучше вместе не использовать. Команда price позволяет ограничить предполагаемую сумму чека.\nПри использовании каждой из этих команд бот предложит ввести соответственно адрес, название станции метро или сумму с помощью клавиатуры.\nКоманда cuisine позволяет выбрать кухню.\n\nЗапрос после введения всех данных отправляется с помощью команды search.\n\nПриятного пользования!',reply_markup=item)



#чистилка параметров
@bot.message_handler(commands=['cancel'])
def cancelling (message) :
    prms = {'district[]':'','metro[]':[],'cuisine[]':'','bill[]':[]}
    item = menu()
    bot.send_message(message.from_user.id,'Данные запросов очищены '+emoji.emojize(':ok_hand:',use_aliases=True)+'\nМожно начинать заново',reply_markup=item)


#?page=1
#тут надо доработать
@bot.message_handler(commands=['search'])
def searching (message) :
    req='https://msk.allcafe.ru/catalog/?query='
    names, addresses = {},[]
    html = requests.get(req, params = prms) #запрос на сайт
    print (html.request.url)
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
        b = name.name
        b = b.split('"')
        b = b[1]
        links.append(b)
    for i in range (len(soup.find_all('span', {'class':'placeList_addr'}))) : #ищет адреса мест в том же порядке
        addr = soup.find_all('span', {'class':'placeList_addr'})[i]
        a = addr.text.strip()
        a = a.replace('\n','')
        a = a.replace('  ','')
        addresses.append(a)
    n = 0 #счетчик
    for i in names.keys() :
        names[i] = addresses[n]
        n += 1 #счетчик
#    out = telebot.types.InlineKeyboardMarkup()
    for k, v in names.items() :
        print(k,v)
    print (links



#все сложно с текстовыми сообщениями, поэтому тут одна функция, которая на самом деле разная
@bot.message_handler(content_types=['text'])
#def getting_text_messages (message,flag=flag) :
#    if flag[0] == '0' : #дефолтный вариант
 #       item = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True).row('/help')
  #      bot.send_message(message.chat.id,'Не понимаю, что ты хочешь сказать. Попробуй воспользоваться кнопкой /help',reply_markup=item)
   # elif flag[0] == '1' : #для функции определения цены
    #    price = message.text
     #   with open ('price.json', 'r', encoding='utf-8') as f :
      #      Price = json.load(f)
       # for k in Price.keys() :
        #    if int(k) <= int(price) :
         #       prms['bill[]'].append (Price[k])
#        print(prms)
 #       bot.send_message(message.from_user.id,emoji.emojize(':ok_hand:',use_aliases=True),reply_markup=menu())
  #      flag = 0
   # elif flag[0] == '2' : #для функции определения метро
    #    metro = message.text
     #   with open ('metro.json', 'r', encoding='utf-8') as f :
      #      Metro = json.load(f)
       # prms['metro[]'] = Metro.get(metro.lower(),'арбатская') #чтоб если чего-то нет в списке, он не сломался
        #print(prms)
        #bot.send_message(message.from_user.id,emoji.emojize(':ok_hand:',use_aliases=True),reply_markup=menu())
        #flag = 0
#    elif flag[0] == '3' : #для функции определения адреса
 #       address = 'Москва '+message.text
  #      with open ('metro.json', 'r', encoding='utf-8') as f :
   #         Metro = json.load(f)
    #    with open ('districts.json', 'r', encoding='utf-8') as f :
     #       Districts = json.load(f)
      #  dadata = Dadata(conf.a,conf.b)
       # address = dadata.clean('address', address)
        #district = address['city_district'].strip().lowercase()
#        if isinstance(address['metro'],list) : #может быть несколько станций метро или одна
 #           for i in address['metro'] :
  #              prms['metro[]'].append (Metro.get(i['name'].strip().lower(),'арбатская')) #чтоб если чего-то нет в списке, он не сломался
   #     else :
    #        prms['metro[]'] = Metro.get(address['metro'],'арбатская')
     #   prms['district[]'] = Districts.get(district,'арбат') #чтоб если чего-то нет в списке, он не сломался
      #  print(prms)
       # bot.send_message(message.from_user.id,emoji.emojize(':ok_hand:',use_aliases=True),reply_markup=menu())
        #flag = 0
        


if __name__ == '__main__':
    bot.polling(none_stop=True)
