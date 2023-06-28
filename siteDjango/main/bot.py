import telebot
from telebot import types

# Создаем экземпляр бота
bot = telebot.TeleBot('6124448012:AAFch7qEIjF2iKBoFZEL4yEcB008oqanDdU')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
#     # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Меню')
    itembtn2 = types.KeyboardButton('Связь с оператором')
    markup.add(itembtn1, itembtn2)

#     # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        


@bot.message_handler(commands=['menu'])
def send_links(message):
    # Создаем клавиатуру с кнопками-ссылками
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='В банк', url='http://127.0.0.1:8000/')
    itembtn2 = types.InlineKeyboardButton(text='Специальные предложения', url='http://127.0.0.1:8000/client/offers')
    markup.add(itembtn1, itembtn2)

    # Отправляем сообщение с клавиатурой-ссылками
    bot.send_message(message.chat.id, "Меню:", reply_markup=markup)




# Обработчик нажатия на кнопки
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "Меню":
        bot.send_message(message.chat.id, send_links(message))
    elif message.text == "Связь с оператором":
        bot.reply_to(message, "Связь")



# Запускаем бота
bot.polling()