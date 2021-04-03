import telebot


bot = telebot.TeleBot('1759437165:AAFDzo_WExxQu7uqlZNLHcXkU4fbJdk1GU4')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')
    
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Я бот. Приятно познакомиться, {message.from_user.first_name}')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')

if __name__ == '__main__':
    bot.polling(none_stop=True)
