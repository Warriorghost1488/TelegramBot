import telebot
from utilts import APIExeption, Converter
from config import exchanges, TOKEN
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message:telebot.types.Message):
    text = "Для начала работы с ботом необзходимо ввести команду в следующем формате:\n <Валюта цену которой хотите узнать>\
    <Валюта в которую надо перевести> \
    <Количство переводимой валюты> \n Чтобы получить список доступных валют введите команду: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in exchanges.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message:telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIExeption('Не верный ввод')

        answer = Converter.get_price(*values)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя \n"{e}"')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)