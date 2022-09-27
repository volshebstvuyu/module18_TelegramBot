import telebot
from our_token import token
from constants import *
from extensions import *

TOKEN = token
# TOKEN = _token

bot = telebot.TeleBot(TOKEN)

# обработчик команд
@bot.message_handler(commands=['start'])
def handle_start_command(message):
    text = f'Приветствую, {message.chat.first_name}. Я - бот. Моя задача получить от тебя команду (/start, /help, /values) или 3 параметра для исчисления конвертации\n' \
           f'\nКонвертация происходит по следующим правиламвы мне 3 параметра через пробел в виде <исходная валюта> <валюта в которую надо перевести> <количество у.е.>, а я вам результат выдаю'
    bot.reply_to(message, text)\


@bot.message_handler(commands=['help'])
def handle_help_command(message):
    text = f'{message.chat.first_name}, конвертация валюты происходит по следующим правилам: вы мне 3 параметра через пробел в виде <исходная валюта> <валюта в которую надо перевести> <количество у.е.>, а я вам результат выдаю'
    bot.reply_to(message, text)


# обработчик команды /values
@bot.message_handler(commands=['values'])
def handle_values(message):
    text = 'Доступные валюты:'
    for item in currency.keys():
        text += f'\n\t\t{item}'
    bot.reply_to(message, text)


# здесь обрабатывается входящее сообщение состоящие из исходной валюты
@bot.message_handler(content_types=["text"])
def handle_request(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            bot.reply_to(message, 'Параметров должно быть 3, а ты сколько прислал? БОЛЬШЕ!!')
        elif len(values) < 3:
            bot.reply_to(message, 'Такая простая просьба и то слабоват =( Я просил 3 аргумента, никак не меньше!')
        else:
            base, quote, amount = values
            total_quote = Exchange.get_price(base, quote, amount)
    except Exception as e:
        if type(e) == APIException:
            bot.reply_to(message, f'Ошибка пользователя. Лузер\n\n{e}')
        bot.reply_to(message, f'Что-то пошло не так.\n\n{e}')
    for key, value in currency.items():
        if base in value:
            base = key
        if quote in value:
            quote = key

    text = f'Первод из {base} в {quote} состоялся:\n{amount} {base} = {total_quote} {quote}'

    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)