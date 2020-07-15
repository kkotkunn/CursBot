import telebot
import config
import api
import json


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def command(message):
    if message.text == '/start':
        bot.send_message(
            message.chat.id,
            'Привет. Я покажу тебе курс гривен (UAH).\n' +
            'Чтобы узнать курсы обмена, нажми  /exchange.\n' +
            'Чтобы узнать о боте, нажми  /about.\n' +
            'Чтобы узнать как я работаю нажми /help.'
        )
    elif message.text == '/about':

        bot.send_message(
            message.chat.id,
            'Для получения информации бот использует PrivatBank API. \n' +
            'URL для перехода на сайт https://api.privatbank.ua/#p24/exchange .\n' +
            'Были использованы Python,библиотеки: pyTelegramBotAPI,requests.'
        )
    elif message.text == '/help':
        bot.send_message(
            message.chat.id,
            '1) Чтобы получить список доступных валют, нажми /exchange.\n' +
            '2) Нажми на интересующую тебя валюту.\n' +
            '3) Ты получишь сообщение с нужной информацией.\n' +
            '4) Ты можешь нажимать на другие валюты, не нажимая еще раз /exchange.\n' +
            '5) Чтобы узнать о боте, нажми /about',
        )

    elif message.text == '/exchange':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('USD (доллар)', callback_data='get-USD')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('EUR (евро)', callback_data='get-EUR'),
            telebot.types.InlineKeyboardButton('RUR (рубли)', callback_data='get-RUR')
        )

        bot.send_message(
            message.chat.id,
            'Выбери валюту:',
            reply_markup=keyboard
        )

    else:
        bot.send_message(message.chat.id, 'Я не знаю что ответить, используй /help или команды при /start ')


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('get-'):
        get_ex_callback(query)


def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange_result(query.message, query.data[4:])


def send_exchange_result(message, ex_code):
    bot.send_chat_action(message.chat.id, 'typing')
    ex = api.get_exchange(ex_code)
    bot.send_message(
        message.chat.id, serialize_ex(ex),

        parse_mode='HTML'
    )


def get_update_keyboard(ex):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Update',
            callback_data=json.dumps({
                't': 'u',
                'e': {
                    'b': ex['buy'],
                    's': ex['sale'],
                    'c': ex['ccy']
                }
            }).replace(' ', '')
        ),
        telebot.types.InlineKeyboardButton('Share', switch_inline_query=ex['ccy'])
    )
    return keyboard


def serialize_ex(ex_json):
    result = '<b>' + ex_json['base_ccy'] + ' -> ' + ex_json['ccy'] + ':</b>\n\n' + \
             'Курс покупки:  ' + ex_json['buy']

    result += '\nКурс продажи:  ' + ex_json['sale'] + '\n'
    return result

bot.polling(none_stop=True)
