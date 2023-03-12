from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import default_tickers
from utils import Convertor


def kb_keypad():
    keypad = InlineKeyboardMarkup(row_width=4, one_time_keyboard=True)

    keypad.row(InlineKeyboardButton('1⃣', callback_data='1'),
               InlineKeyboardButton('2️⃣', callback_data='2'),
               InlineKeyboardButton('3️⃣', callback_data='3'),
               InlineKeyboardButton('🔙 correct', callback_data='<='))

    keypad.row(InlineKeyboardButton('4⃣️', callback_data='4'),
               InlineKeyboardButton('5⃣', callback_data='5'),
               InlineKeyboardButton('6⃣', callback_data='6'),
               InlineKeyboardButton('❌ clear', callback_data='cls'))

    keypad.row(InlineKeyboardButton('7⃣', callback_data='7'),
               InlineKeyboardButton('8⃣', callback_data='8'),
               InlineKeyboardButton('9️⃣', callback_data='9'),
               InlineKeyboardButton('Help', callback_data='Help'))

    keypad.row(InlineKeyboardButton('.', callback_data='.'),
               InlineKeyboardButton('0⃣', callback_data='0'),
               InlineKeyboardButton('000', callback_data='000'),
               InlineKeyboardButton('Enter', callback_data='Enter'))
    return keypad


kb_numpad = kb_keypad()


def kb_currency(tickers: tuple = default_tickers):
    currencies = Convertor.get_currencies(tickers)
    dc = currencies  # Displayed currencies { "RUB": "Российский рубль", ..}
    t = [*dc]  # Tickers ['RUB', 'USD', 'EUR', ..]

    kb_curr = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)

    kb_curr.row(InlineKeyboardButton(f"{t[0]}: {dc[t[0]]}", callback_data=f"{t[0]}"),
                InlineKeyboardButton(f"{t[1]}: {dc[t[1]]}", callback_data=f"{t[1]}"))

    kb_curr.row(InlineKeyboardButton(f"{t[2]}: {dc[t[2]]}", callback_data=f"{t[2]}"),
                InlineKeyboardButton(f"{t[3]}: {dc[t[3]]}", callback_data=f"{t[3]}"))

    kb_curr.row(InlineKeyboardButton(f"{t[4]}: {dc[t[4]]}", callback_data=f"{t[4]}"),
                InlineKeyboardButton(f"{t[5]}: {dc[t[5]]}", callback_data=f"{t[5]}"))

    kb_curr.row(InlineKeyboardButton(f"{t[6]}: {dc[t[6]]}", callback_data=f"{t[6]}"),
                InlineKeyboardButton(f"{t[7]}: {dc[t[7]]}", callback_data=f"{t[7]}"))

    return kb_curr


def kb_result(result: str = "Нет данных = Нет данных"):
    res = result.split('=')
    kb_res = InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
    kb_res.row(InlineKeyboardButton(f"{res[0]} =", callback_data=f"Result_from"))
    kb_res.row(InlineKeyboardButton(f"{res[1]}", callback_data=f"Result_to"))
    kb_res.row(InlineKeyboardButton("Ввод новых данных", callback_data=f"New"))
    return kb_res


# ___________________________________________________________
#   ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# ___________________________________________________________
