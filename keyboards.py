from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import default_tickers
from utils import Convertor


class MyInlineKeyboard:
    def __init__(self):
        self.tickers = default_tickers
        self.default_currencies = self.get_default_currencies
        self.keypad = self.kb_keypad
        self.currency = self.kb_currency
        # self.currency = self.kb_currency(dt)
        # self.default_currencies = {}

    @property
    def get_default_currencies(self):
        return Convertor().get_default_currencies(self.tickers)

    @property
    def kb_keypad(self):
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

    @property
    def kb_currency(self):
        dc = self.default_currencies  # Default currencies { "RUB": "Российский рубль", ..}
        t = [*dc]  # Tickers ['RUB', 'USD', 'EUR', ..]
        # dc = Convertor().get_default_currencies(self.tickers)  # Default currencies { "RUB": "Российский рубль", ..}
        # print("===== dc=KEYBoards==", dc, t)

        currency = InlineKeyboardMarkup(row_width=2, one_time_keyboard=True)

        currency.row(InlineKeyboardButton(f"{t[0]}: {dc[t[0]]}", callback_data=f"{t[0]}"),
                     InlineKeyboardButton(f"{t[1]}: {dc[t[1]]}", callback_data=f"{t[1]}"))

        currency.row(InlineKeyboardButton(f"{t[2]}: {dc[t[2]]}", callback_data=f"{t[2]}"),
                     InlineKeyboardButton(f"{t[3]}: {dc[t[3]]}", callback_data=f"{t[3]}"))

        currency.row(InlineKeyboardButton(f"{t[4]}: {dc[t[4]]}", callback_data=f"{t[4]}"),
                     InlineKeyboardButton(f"{t[5]}: {dc[t[5]]}", callback_data=f"{t[5]}"))

        currency.row(InlineKeyboardButton(f"{t[6]}: {dc[t[6]]}", callback_data=f"{t[6]}"),
                     InlineKeyboardButton(f"{t[7]}: {dc[t[7]]}", callback_data=f"{t[7]}"))

        return currency


# -----------------------------------------------
# button1 = KeyboardButton('RUB')
# button2 = KeyboardButton('USD\nДоллар')
# button3 = KeyboardButton('EUR\nЕвро')
#
# currency1 = ReplyKeyboardMarkup()
# currency1.row(button1, button2, button3)
# currency1.row(button1, button2, button3)
# ----------------------------------------------------
# ====================================================
# ----------------------------------------------------------------
# cur = Convertor.get_symbols()  # currencies

# Для поиска:
# Можно инвертировать словарь inv_d = {value: key for key, value in d.items()}

# Использовать вместо  dc[0] и cur[dc[0] :
# >>> d     # {'AED': 'Дирхам ОАЭ', 'BDT': 'Бангладешская така'}
# >>> [*dc][1]       # 'BDT'
# >>> dc[[*dc][1]]        # 'Бангладешская така'
# ----------------------------------------------------------------
# InlineKeyboardButton('0⃣0⃣0⃣', callback_data=' 000'),

# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------
# currency = ReplyKeyboardMarkup().add(
#     button1).add(button2).add(button3)
# InlineKeyboardButton('🔙 backspace', callback_data='<='))
# InlineKeyboardButton('USD Доллар', callback_data='USD'),
# InlineKeyboardButton('Евро: EUR', callback_data='EUR'))
# InlineKeyboardButton('CHF Швейцарский франк', callback_data='CHF'),
# InlineKeyboardButton('CNY: Китайский юань', callback_data='CNY'))
# InlineKeyboardButton('ILS', callback_data='ILS'),
# InlineKeyboardButton('JPY', callback_data='JPY'))
# currency.row(InlineKeyboardButton('INR: Индийская рупия', callback_data='INR"'),
#              # InlineKeyboardButton('SEK Шведская крона', callback_data='SEK'),
#              InlineKeyboardButton('JPY: Японская иена', callback_data='JPY'))
#            # InlineKeyboardButton('SGD', callback_data='SGD'))
#
# currency.row(InlineKeyboardButton('CAD: Канадский доллар', callback_data='CAD'),
#              # InlineKeyboardButton('BYR Белорусский рубль', callback_data='BYR'),
#              InlineKeyboardButton('CZK: Чешская крона', callback_data='CZK'))
#            # InlineKeyboardButton('EGP', callback_data='EGP'))
