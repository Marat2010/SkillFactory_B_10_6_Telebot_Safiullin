
from config import TOKEN_TG, help_start, help_message, default_tickers, headers
# import ujson
import logging
from aiogram import Bot, Dispatcher, executor, types
from utils import Convertor, ConvertException

from keyboards import MyInlineKeyboard
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)

NUMBER = ''
OLD_NUMBER = ''


# --------------------------------

# @dp.message_handler(commands=['currency'])
# async def currency_command(message: types.Message):
#     await message.reply("Выбор валюты",
#                         reply_markup=kb.currency1)


# @dp.message_handler(commands=['rm'])
# async def process_rm_command(message: types.Message):
#     await message.reply("Убираем шаблоны сообщений",
#                         reply_markup=kb.ReplyKeyboardRemove())


# @dp.message_handler(commands=['keypad'])

@dp.message_handler(commands=['list'])
async def list_currencies(message: types.Message):
    url_list = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_" \
               "%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D1%83%D1%8E%D1%89%D0%B8%D1%85_" \
               "%D0%B2%D0%B0%D0%BB%D1%8E%D1%82"
    await message.answer(f"Список доступных валют и их коды\n {url_list}")


@dp.message_handler(commands=['change'])
async def change_currency_keyboard(message: types.Message):
    global NUMBER

    tickers = message.text.split()
    print(f"==CHANGE=tickers= {tickers}")
    tickers, change_tic = Convertor().check_currency(tickers)
    change_tic = ', '.join(change_tic)
    print(f"=Check=CHANGE=tickers= {tickers} == {change_tic}")
    print(f"==CHANGE==1== {message.text} =={kb.tickers}")

    kb.tickers = tickers
    kb.default_currencies = kb.get_default_currencies
    kb.currency = kb.kb_currency

    print(f"==CHANGE==2== kb.tickers =={kb.tickers}")
    print(f"==CHANGE==3== kb.default_currencies ==={kb.default_currencies}")
    print(f"==CHANGE==4== kb.currency =={kb.currency}")

    NUMBER = ''
    print(f"=== NUMBER== {NUMBER}")

    await message.answer(f"В список валют внесены изменения ({change_tic})")
    await message.answer("0", reply_markup=kb.keypad)


@dp.message_handler(commands=['default'])
async def default_currency_keyboard(message: types.Message):
    global NUMBER

    kb.tickers = default_tickers
    kb.default_currencies = kb.get_default_currencies
    kb.currency = kb.kb_currency
    print(f"==CHANGE Default= {message.text} == ", kb.kb_currency)

    NUMBER = ''
    print(f"=== NUMBER== {NUMBER}")

    await message.answer("Список валют установлен по умолчанию")
    await message.answer("0", reply_markup=kb.keypad)


@dp.message_handler(commands=['convert'])
async def numeric_keypad(message: types.Message):
    global NUMBER, OLD_NUMBER
    if NUMBER == '':
        await message.answer("0", reply_markup=kb.keypad)
    else:
        await message.answer(NUMBER, reply_markup=kb.keypad)


@dp.callback_query_handler(lambda call: True)
async def callback_func(callback_query: types.CallbackQuery):
    global NUMBER, OLD_NUMBER
    data = callback_query.data

    # print(f"```` ==={type(callback_query.values)} ===", callback_query.values)  # }]]}} >, 'chat_instance': '7764629237497949216', 'data': '6', '1111': 'qqqq'}
    print(f" === NUMBER+== ", NUMBER)

    if data == 'cls':
        NUMBER = ''
    elif data == '<=':
        NUMBER = NUMBER[:len(NUMBER) - 1]
    elif data == 'Enter':
        print(f"==Number= {NUMBER}, = Тип: {type(NUMBER)}")
        try:
            float(NUMBER)
        except ValueError:
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=f"{NUMBER}: \t - не число!",
                                   reply_markup=kb.keypad)
            raise ConvertException(f"{float(NUMBER)} - не число!")


        # await bot.send_message(chat_id=callback_query.message.chat.id,
        #                        text=f"{NUMBER}: \t сумма в какой Валюте? :",
        #                        reply_markup=types.ReplyKeyboardRemove())
        # await bot.delete_message(chat_id=callback_query.message.chat.id,
        #                          message_id=callback_query.message.message_id)

        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=f"{NUMBER}: \t сумма в какой Валюте? :",
                               reply_markup=kb.kb_currency)
    elif data == 'Help':
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text=help_message)
    # elif data in default_tickers:
    elif data in kb.tickers:
        print('=== In def ===', callback_query.values)
        # callback_query.from_ticker = data
        # from_ticker = callback_query.values.get('from_ticker')

        # print(f"==== from_ticker === {from_ticker}")
        # print("==DOOOO = callback_query.from_ticker=== ", callback_query.from_ticker)
        NUMBER += f" {data}"
        from_ticker = NUMBER.split()
        print("==from_ticker=== ", from_ticker)

        if len(from_ticker) == 2:
            from_ticker = from_ticker[1]
            # from_ticker = data
            # callback_query.values['from_ticker'] = data
            # callback_query.from_ticker = data
            # print("==callback_query.values['from_ticker']=== ", callback_query.values['from_ticker'])
            # await bot.send_message(chat_id=callback_query.message.chat.id,
            #                        text=f"{NUMBER} {data}")
            print("==from_ticker=== ", from_ticker)

            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=f"{NUMBER}: \t в какую Валюту перевести? :",
                                        reply_markup=kb.kb_currency)
    else:
        NUMBER += data

    if NUMBER != OLD_NUMBER:
        if NUMBER == '':
            # converted_text = f"{NUMBER} {from_ticker} ({kb.default_currencies[from_ticker]}) = {converted_sum} {to_ticker} ({kb.default_currencies[to_ticker]})"
            # converted_text = "111111111111111"
            # await bot.send_message(chat_id=callback_query.message.chat.id,
            #                        text=converted_text)

            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text='0', reply_markup=kb.keypad)
        elif len(NUMBER.split()) == 2:
            pass
        elif len(NUMBER.split()) == 3:
            NUMBER, from_ticker, to_ticker = NUMBER.split()
            print(f"---- From3 === {NUMBER.split()}")
            # await message.answer(f"В список валют внесены изменения ({change_tic})")
            # print(f"---- From4 === {Convertor().russ_dict}")
            print(f"---- From4 === {kb.tickers}")
            print(f"---- From4 === {kb.default_currencies[from_ticker]}")
            print(f"---- From5 === {kb.default_currencies[to_ticker]}")

            converted_sum = 123.45
            converted_text = f"{NUMBER} {from_ticker} ({kb.default_currencies[from_ticker]}) = " \
                             f"{converted_sum} {to_ticker} ({kb.default_currencies[to_ticker]})"

            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=f"{NUMBER} {from_ticker} ({kb.default_currencies[from_ticker]}) "
                                        f"= {converted_sum} "
                                        f"{to_ticker} ({kb.default_currencies[to_ticker]})")

            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=converted_text,
                                        reply_markup=kb.keypad)

            NUMBER = ''

        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=NUMBER, reply_markup=kb.keypad)
            # text=NUMBER, reply_markup=kb.currency)

    OLD_NUMBER = NUMBER


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer(help_message)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global kb
    kb = MyInlineKeyboard()  # Инициализация параметров
    await message.answer(help_start)


@dp.message_handler(content_types=['text'])
async def currency_command(message: types.Message):
    # pass
    print(f" === TEXT 22+== ", await bot.get_session())

# ___________________________________________________________________________

    # print(f" ==mes1 =={message}")
    # if message.text == 'RUB':
    #     print(f" ==mes2 =={message}")
    #     print(f" ==mes3 =={dp.callback_query_handlers.dispatcher.__dict__}")
    #     await message.answer("На что менять? ", reply_markup=kb.kb_currency)
    # elif message.text == 'EUR':
    #     await message.answer("Результ = ", reply_markup=kb.keypad)
# ___________________________________________________________________________
# ___________________________________________________________________________


# ----------------------------------------
# help - Помощь
# convert - Ковертор валют
# @dp.message_handler(commands=['2'])
# async def process_command_2(message: types.Message):
#     await message.reply("Отправляю все возможные кнопки",
#                         reply_markup=kb.inline_kb_full)
#
#
# @dp.message_handler()
# async def echo(message: types.Message):
#     print(f"====MESSAGE== {message} \nTYPE=== {type(message)}")
#     await message.answer(message.text)


if __name__ == '__main__':
    kb = MyInlineKeyboard()  # Инициализация параметров
    executor.start_polling(dp, skip_updates=True)

# --------------------------------------------------
# help - Описание
# convert - Конвертер валют
# default - Список валют по умолчанию
# list - Список доступных валют и их коды
# change - Изменить последние 4 валюты
# (/change AED BYR IRR KGS)
#
#
# help - Описание
# convert - Конвертер валют
# default - Сбросить список валют по умолчанию
# change AED BYR IPR KGS - Изменить последие 4 валюты
# --------------------------------------------------
    # cb953 = {'id': '1037071880219144011',
    #          'from': {
    #              "<User": {
    #                  "id": 241462113, "is_bot": False, "first_name": "Marat", "last_name": "S", "username": "Marat2010",
    #                  "language_code": "ru"}
    #          }, 'message': {"<Message": {"message_id": 1644,
    #                                      "from": {"id": 6065866125, "is_bot": True, "first_name": "Exchange rates",
    #                                               "username": "RuChyExch_Bot"},
    #                                      "chat": {"id": 241462113, "first_name": "Marat", "last_name": "S",
    #                                               "username": "Marat2010", "type": "private"}, "date": 1677802371,
    #                                      "edit_date": 1677802385, "text": "111", "reply_markup": {"inline_keyboard": [
    #             [{"text": "1⃣", "callback_data": "1"}, {"text": "2️⃣", "callback_data": "2"},
    #              {"text": "3️⃣", "callback_data": "3"}, {"text": "🔙 correct", "callback_data": "<="}],
    #             [{"text": "4⃣️", "callback_data": "4"}, {"text": "5⃣", "callback_data": "5"},
    #              {"text": "6⃣", "callback_data": "6"}, {"text": "❌ clear", "callback_data": "cls"}],
    #             [{"text": "7⃣", "callback_data": "7"}, {"text": "8⃣", "callback_data": "8"},
    #              {"text": "9️⃣", "callback_data": "9"}, {"text": "Help", "callback_data": "Help"}],
    #             [{"text": ".", "callback_data": "."}, {"text": "0⃣", "callback_data": "0"},
    #              {"text": "000", "callback_data": "000"}, {"text": "Enter", "callback_data": "Enter"}]]}}
    #                         },
    #          'chat_instance': '7764629237497949216',
    #          'data': 'Enter'
    #          }
    #
    # cb937 = {'id': '5731653147129621793',
    #          'from': {
    #              "<User": {"id":5629471787,"is_bot":False,"first_name":"Марат","last_name":"Са","username":"Marat937","language_code":"ru"}
    #          },
    #         'message': {
    #             "<Message": {"message_id":1648,"from":{"id":6065866125,"is_bot":True,"first_name":"Exchange rates","username":"RuChyExch_Bot"},"chat":{"id":5629471787,"first_name":"Марат","last_name":"Са","username":"Marat937","type":"private"},"date":1677803433,"edit_date":1677803434,"text":"INR98855","reply_markup":{"inline_keyboard":[[{"text":"1⃣","callback_data":"1"},{"text":"2️⃣","callback_data":"2"},{"text":"3️⃣","callback_data":"3"},{"text":"🔙 correct","callback_data":"<="}],[{"text":"4⃣️","callback_data":"4"},{"text":"5⃣","callback_data":"5"},{"text":"6⃣","callback_data":"6"},{"text":"❌ clear","callback_data":"cls"}],[{"text":"7⃣","callback_data":"7"},{"text":"8⃣","callback_data":"8"},{"text":"9️⃣","callback_data":"9"},{"text":"Help","callback_data":"Help"}],[{"text":".","callback_data":"."},{"text":"0⃣","callback_data":"0"},{"text":"000","callback_data":"000"},{"text":"Enter","callback_data":"Enter"}]]}}
    #         },
    #          'chat_instance': '8015743227589537572',
    #          'data': '9'
    #          }
    #
    # with open('callback_query_values_937.json', 'w', encoding='utf-8') as f:
    #     ujson.dump(cb937, f, indent=4, ensure_ascii=False)

# --------------------------------------------------
# from keyboards import keypad, currency
# import keyboards as kb
# Configure logging
    # tickers = ['SBD', 'VEF', 'EUR', 'BTC', 'CNY', 'XAG', 'CHF', 'GBP']

# --------------------------------------------------
# bot1.answer_callback_query(callback_query.id, text='0')
# await bot.edit_message_text(text='0', reply_markup=keyboard)
# bot1.answer_callback_query(callback_query.id, text=number)
# await bot.edit_message_text(text=number, reply_markup=keyboard)
# await message.reply("0", reply_markup=keyboard)
# await message.reply("Cумма: ", reply_markup=keyboard)

# --------------------------------------------------
# @dp.message_handler(commands=['hi5'])
# async def process_hi5_command(message: types.Message):
#     await message.reply("Пятое - добавляем ряды кнопок",
#                         reply_markup=kb.markup5)
#
#
# @dp.message_handler(commands=['hi7'])
# async def process_hi7_command(message: types.Message):
#     await message.reply("Седьмое - все методы вместе",
#                         reply_markup=kb.markup_big)
#
#
# @dp.message_handler(commands=['rm'])
# async def process_rm_command(message: types.Message):
#     await message.reply("Убираем шаблоны сообщений",
#                         reply_markup=kb.ReplyKeyboardRemove())
#
#
# # ---------- inline kb -----
#
# @dp.message_handler(commands=['1'])
# async def process_command_1(message: types.Message):
#     await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)

# --------------------------------------------------
# @dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
# async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
#     code = callback_query.data[-1]
#     if code.isdigit():
#         code = int(code)
#     if code == 2:
#         await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
#     elif code == 5:
#         await bot.answer_callback_query(
#             callback_query.id,
#             text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉',
#             show_alert=True)
#     else:
#         await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')
# ##
# --------------------------------------------------
# bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard())
# ---------------------------------
# bot.send_message(
#   chat_id=uid, reply_markup=kb_fruits,
#   text="Please select one of the fruit:")
# ---------------------------------

# @dp.message_handler(commands=['fr'])
# async def fr_command(message: types.Message):
#     bot1.send_message(chat_id=message.chat.id,
#                       reply_markup=kb_fruits(), text='zzz')

# --------------------------------------------------
# @dp.message_handler(commands=['qq'])
# async def qq_command(message: types.Message):
#     print(f"----MES= {message.chat.id}")
#     # await message.reply("qqqПривет!", reply_markup=kb.greet_keybo1)
#     # await message.answer("qqqПривет!", reply_markup=keybo1())
#     bot1.send_message(chat_id=message.chat.id, text='zzz',
#                            reply_markup=keybo1())
# --------------------------------------------------
# bot1 = telebot.TeleBot(token=TOKEN_TG)
# import telebot
# --------------------------------------------------
# from aiogram.dispatcher import Dispatcher
# from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup,\
#     KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


# -----------------------------------------------------
# from aiogram import Bot, types
# from aiogram.utils import executor
# from aiogram.utils.markdown import text

# -----------------------------------------------------
# --------------------------
# button_hi = KeyboardButton('Привет! 👋')
#
# greet_kb = ReplyKeyboardMarkup()
# greet_kb.add(button_hi)
# ------------------------

# --------------------------------------------------