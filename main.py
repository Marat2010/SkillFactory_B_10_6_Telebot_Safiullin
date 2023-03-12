# import redis
# from aiogram.utils import json
# from redis.commands import json
# import ujson
# import logging
# logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher

from config import TOKEN_TG, help_start, help_message, default_tickers, url_list, headers
from aiogram import Bot, Dispatcher, executor, types

from utils import Convertor, Chat, digit_check, ConvertException, red
from keyboards import kb_numpad, kb_currency, kb_result

bot = Bot(token=TOKEN_TG)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'default'])
async def process_start_command(message: types.Message):
    """
    Инициализация параметров чата (Или сброс)
    """
    chat_values = {'input_str': '',
                   'tickers': default_tickers,
                   'currencies': Convertor.get_currencies(),
                   'kb_currency': kb_currency(),
                   # 'old_input_str': '',
                   # 'result': []
                   }
    Chat.set_chat_data(message.chat.id, chat_values)

    if message.text == '/start':
        await message.answer(help_start)
    else:
        await message.answer("Список валют установлен по умолчанию")
        await message.answer("0", reply_markup=kb_numpad)


@dp.message_handler(commands=['convert'])
async def numeric_keypad(message: types.Message):
    Chat.set_chat_data(message.chat.id, {'input_str': ''})
    await message.answer("0", reply_markup=kb_numpad)


@dp.callback_query_handler(lambda call: True)
async def callback_func(callback_query: types.CallbackQuery):
    data = callback_query.data

    # Загрузка данных чата
    settings = Chat.get_chat_data(callback_query.message.chat.id)

    input_str = settings.get('input_str')
    tickers = settings.get('tickers')
    currencies = settings.get('currencies')
    kb_curr = settings.get('kb_currency')
    # result = settings.get('result')
    # old_input_str = settings['old_input_str']

    print(f"==SETTINGS-input_str: {input_str} -keys-- {settings.keys()}")

    if data == 'cls':
        if input_str:
            input_str = ''
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text='0', reply_markup=kb_numpad)

    elif data == '<=':
        if len(input_str):
            input_str = input_str[:len(input_str) - 1]
            sh_input_str = digit_check(input_str)[1] or '0'  # 0 - Если пустая строка

            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=sh_input_str, reply_markup=kb_numpad)

    elif data == 'Enter':
        num, str_out = digit_check(input_str)  # num: число или False, str_out: строка для вывода
        if num:
            sh_input_str = f"{str_out}  -  эта сумма в какой Валюте? :"
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=sh_input_str, reply_markup=kb_curr)
        else:
            sh_input_str = f"{input_str}  -  Это не число!!!"
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=sh_input_str, reply_markup=kb_numpad)
            input_str = "0"

    elif data == 'Help':
        await bot.send_message(chat_id=callback_query.message.chat.id, text=help_message)

    elif data in tickers:
        input_str += f"  {data}"
        print('=== Data in Tickers ===: ', input_str)

        if len(input_str.split()) == 2:
            num, str_out = digit_check(input_str.split()[0])  # num: число или False, str_out: строка для вывода
            sh_input_str = (str_out + f" {data}") if num else f"{input_str.split()[0]}  -  Это не число!!!"

            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=f"{sh_input_str}  -  в какую Валюту перевести? :",
                                        reply_markup=kb_curr)

        elif len(input_str.split()) == 3:
            input_str, from_ticker, to_ticker = input_str.split()

            num, str_out = digit_check(input_str)  # num: число или False, str_out: строка для вывода
            sh_input_str = str_out if num else f"{input_str}  -  Это не число!!!"

            if from_ticker == to_ticker:
                converted_sum = f" Валюты должны быть разными!!!"
            else:
                # converted_sum = 173123.45113
                converted_sum = Convertor.get_price(num, from_ticker, to_ticker)

                converted_sum = f"{converted_sum: _.2f}"
                print(f"==CONVERTed_sum =: {converted_sum}")

            converted_text = f"{sh_input_str}  {from_ticker} ({currencies[from_ticker]})  =" \
                             f"  {converted_sum}  {to_ticker} ({currencies[to_ticker]})\n"
                             # f"  {converted_sum}  {to_ticker} ({currencies[to_ticker]})\n"

            settings['result'] = [sh_input_str, from_ticker, converted_sum, to_ticker]

            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=converted_text,
                                        reply_markup=kb_result(converted_text))

            input_str = ''  # Осторожно с этим здесь

    elif data == 'Result_from' or data == 'Result_to' or data == 'New':
        if data == 'New':
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text="0", reply_markup=kb_numpad)
        else:
            settings = Chat.get_chat_data(callback_query.message.chat.id)
            result = settings.get('result')
            # message_id = settings.get('message_id')

            input_str = f"{result[0]} {result[1]}" if data == 'Result_from' else f"{result[2]} {result[3]}"

            print(f"==== Res =={callback_query.message.message_id}=={result}==")

            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=f"{input_str}  -  в какую Валюту перевести? :",
                                   reply_markup=kb_curr)

    else:  # Здесь обработка ввода чисел на numpad
        input_str += data

        num, str_out = digit_check(input_str)  # num: число или False, str_out: строка для вывода
        if num:
            sh_input_str = str_out
        else:
            sh_input_str = f"{input_str}  -  Это не число!!!"
            input_str = "0"

        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=sh_input_str, reply_markup=kb_numpad)

    # Сохранение данных чата
    settings['input_str'] = input_str
    Chat.set_chat_data(callback_query.message.chat.id, settings)
    print(f"  === OUTPUT=== Settings==: {settings}")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer(help_message)


@dp.message_handler(commands=['change'])
async def change_currency_keyboard(message: types.Message):
    tickers = message.text.split()
    chat_tickers, change_tic = Convertor.update_tickers(message.chat.id, tickers)

    chat_values = {'input_str': '',
                   # 'old_input_str': '',
                   'tickers': chat_tickers,
                   'currencies': Convertor.get_currencies(chat_tickers),
                   "kb_currency": kb_currency(chat_tickers)
                   }
    Chat.set_chat_data(message.chat.id, chat_values)

    await message.answer(f"В список валют внесены изменения ({', '.join(change_tic)})")
    await message.answer("0", reply_markup=kb_numpad)


@dp.message_handler(commands=['list'])
async def list_currencies(message: types.Message):
    await message.answer(f"Список доступных валют и их коды\n {url_list}")


@dp.message_handler(content_types=['text'])
async def currency_command(message: types.Message):
    print(f" xxx=== ЭТТО TEXT ==xxx {message} ")
    # pass


if __name__ == '__main__':
    # red.flushall()  # Если надо очистить данные
    executor.start_polling(dp, skip_updates=True)


# --------------------------------------------------------------
# --------------------------------------------------------------
# converted_sum = digit_check(converted_sum)[1]
# print(f"==CONVERTed_sum =: {converted_sum}")
# --------------------------------------------------------------
# num, str_out = digit_check(input_str.split()[0])  # num: число или False, str_out: строка для вывода
# # sh_input_str = (str_out + f" {input_str.split()[1]}") if num else f"{input_str.split()[0]}  -  Это не число!!!"
# sh_input_str = (str_out + f" {data}") if num else f"{input_str.split()[0]}  -  Это не число!!!"
# text=f"{sh_input_str}  -  в какую Валюту перевести? :",
# --------------------------------------------------------------
# print(f"---ELSE--input_str==: {input_str} ==: {sh_input_str}")
# --------------------------------------------------------------
# print(f'=SHOW IF =len:{len(input_str)} =input_str:{input_str} =sh_input_str:{sh_input_str} =')
# --------------------------------------------------------------
# Chat.set_chat_data(callback_query.message.chat.id, settings)

# settings = Chat.get_chat_data(callback_query.message.chat.id)
# message_id = settings.get('message_id')

# await bot.edit_message_text(chat_id=callback_query.message.chat.id,
# await bot.delete_message(chat_id=callback_query.message.chat.id,
#                          # message_id=message_id,)
#                          message_id=callback_query.message.message_id)
#                          # text='remove',
#                          # reply_markup=None)

# await bot.send_message(chat_id=callback_query.message.chat.id,

# --------------------------------------------------------------
# await bot.edit_message_text(chat_id=callback_query.message.chat.id,
#                             message_id=callback_query.message.message_id,
# message_id=message_id,
# settings['message_id'] = callback_query.message.message_id
# message_id = settings.get('message_id')

# --------------------------------

# try:
#     float(input_str)
# except ValueError:
#     await bot.send_message(chat_id=callback_query.message.chat.id,
#                            text=f"{input_str}  -  Это не число!!!",
#                            reply_markup=kb_numpad)
#     Chat.set_chat_data(callback_query.message.chat.id, {'input_str': ''})
# else:
#     await bot.edit_message_text(chat_id=callback_query.message.chat.id,
#                                 message_id=callback_query.message.message_id,
#                                 text=f"{input_str}  -  эта сумма в какой Валюте? :",
#                                 reply_markup=kb_curr)
# --------------------------------

# --------------------------------------------------------------
# @dp.message_handler(commands=['default'])
# async def default_currency_keyboard(message: types.Message):
#     chat_values = {'input_str': '',
#                    'old_input_str': '',
#                    'tickers': default_tickers,
#                    'currencies': Convertor.get_currencies(),
#                    "kb_currency": kb_currency()
#                    }
#     Chat.set_chat_data(message.chat.id, chat_values)
#
#     await message.answer("Список валют установлен по умолчанию")
#     await message.answer("0", reply_markup=kb_numpad)

# --------------------------------------------------------------
# text=converted_text, reply_markup=kb_curr)
# await bot.edit_message_text(chat_id=callback_query.message.chat.id,
# message_id=callback_query.message.message_id,

# --------------------------------------------------------------