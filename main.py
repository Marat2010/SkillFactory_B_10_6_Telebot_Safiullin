from config import TOKEN_TG, help_start, help_message, default_tickers, url_list
from aiogram import Bot, Dispatcher, executor, types

from utils import Convertor, Chat, digit_check, input_str_check, ConvertException
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
                   }
    Chat.update_chat_data(message.chat.id, chat_values)

    if message.text == '/start':
        await message.answer(help_start)
    else:
        await message.answer("Список валют установлен по умолчанию")
        await message.answer("0", reply_markup=kb_numpad)


@dp.message_handler(commands=['convert'])
async def numeric_keypad(message: types.Message):
    Chat.update_chat_data(message.chat.id, {'input_str': ''})
    await message.answer("0", reply_markup=kb_numpad)


@dp.callback_query_handler(lambda call: True)
async def callback_func(callback_query: types.CallbackQuery):
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    # Загрузка данных чата
    settings = Chat.get_chat_data(chat_id)

    input_str = settings.get('input_str')
    tickers = settings.get('tickers')
    kb_curr = settings.get('kb_currency')

    if data == 'cls':
        if input_str:
            input_str = ''
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=callback_query.message.message_id,
                                        text='0', reply_markup=kb_numpad)

    elif data == '<=':
        if len(input_str):
            input_str = input_str[:len(input_str) - 1]
            sh_input_str = digit_check(input_str)[1] or '0'  # 0 - Если пустая строка

            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=callback_query.message.message_id,
                                        text=sh_input_str, reply_markup=kb_numpad)

    elif data == 'Enter':
        num, str_out = digit_check(input_str)  # num: число или False, str_out: строка для вывода
        if num:
            sh_input_str = f"{str_out}  -  эта сумма в какой Валюте? :"
            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=callback_query.message.message_id,
                                        text=sh_input_str, reply_markup=kb_curr)
        else:
            sh_input_str = f"{input_str}  -  Это не число!!!"
            await bot.send_message(chat_id=chat_id,
                                   text=sh_input_str, reply_markup=kb_numpad)
            input_str = "0"

    elif data == 'Help':
        await bot.send_message(chat_id=chat_id, text=help_message)

    elif data in tickers:
        input_str += f"  {data}"

        if len(input_str.split()) == 2:
            num, str_out = digit_check(input_str.split()[0])  # num: число или False, str_out: строка для вывода
            sh_input_str = (str_out + f" {data}") if num else f"{input_str.split()[0]}  -  Это не число!!!"

            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=callback_query.message.message_id,
                                        text=f"{sh_input_str}  -  в какую Валюту перевести? :",
                                        reply_markup=kb_curr)

        elif len(input_str.split()) == 3:
            data_out = input_str_check(chat_id, input_str)  # rez, converted_text, change_tic

            if data_out.get('rez'):
                settings['result'] = Chat.get_chat_data(chat_id)['result']
                await bot.edit_message_text(chat_id=chat_id,
                                            message_id=callback_query.message.message_id,
                                            text=data_out['converted_text'],
                                            reply_markup=kb_result(data_out['converted_text']))
            else:
                await bot.send_message(chat_id=chat_id, text=f"{data_out['converted_text']}")
            input_str = ''  # Осторожно с этим здесь
        else:
            input_str = ''
            await bot.send_message(chat_id=chat_id, text="0", reply_markup=kb_numpad)

    elif data == 'Result_from' or data == 'Result_to' or data == 'New':
        if data == 'New':
            await bot.send_message(chat_id=chat_id,
                                   text="0", reply_markup=kb_numpad)
        else:
            result = settings.get('result')
            input_str = f"{result[0]} {result[1]}" if data == 'Result_from' else f"{result[2]} {result[3]}"

            await bot.send_message(chat_id=chat_id,
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

        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=callback_query.message.message_id,
                                    text=sh_input_str, reply_markup=kb_numpad)

    # Сохранение данных чата
    settings['input_str'] = input_str
    Chat.update_chat_data(chat_id, settings)
    print(f"=== OUTPUT===Settings==input_str=: {settings['input_str']}")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer(help_message)


@dp.message_handler(commands=['change'])
async def change_currency_keyboard(message: types.Message):
    tickers = message.text.split()
    chat_tickers, change_tic = Convertor.update_tickers(message.chat.id, tickers)

    chat_values = {'input_str': '',
                   'kb_currency': kb_currency(chat_tickers)}
    Chat.update_chat_data(message.chat.id, chat_values)

    await message.answer(f"В список валют внесены изменения ({', '.join(change_tic)})")
    await message.answer("0", reply_markup=kb_numpad)


@dp.message_handler(commands=['list'])
async def list_currencies(message: types.Message):
    await message.answer(f"Список доступных валют и их коды\n {url_list}")


@dp.message_handler(content_types=['text'])
async def currency_command(message: types.Message):
    data_out = input_str_check(message.chat.id, message.text)  # rez, converted_text, change_tic

    if data_out.get('change_tic'):   # Обновление клавиатуры валют
        settings = Chat.get_chat_data(message.chat.id)
        settings['kb_currency'] = kb_currency(settings['tickers'])
        Chat.update_chat_data(message.chat.id, settings)

        await message.answer(f"В список валют внесены изменения ({', '.join(data_out['change_tic'])})")

    if data_out.get('rez'):
        await bot.send_message(chat_id=message.chat.id,
                               text=data_out['converted_text'],
                               reply_markup=kb_result(data_out['converted_text']))
    else:
        await message.answer(f"{data_out['converted_text']}")


if __name__ == '__main__':
    # red.flushall()  # Если надо очистить данные
    executor.start_polling(dp, skip_updates=True)

