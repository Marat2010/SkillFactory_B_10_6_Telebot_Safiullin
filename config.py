# from aiogram.utils.markdown import text


# TOKEN_TG = "1444339635:XXXXX-.."
# TOKEN_TG = "1444339635:AAEWaQQmfy-Guk47iioxwIDiT7lbL5h5z-I"
TOKEN_TG = "6065866125:AAHTL1GJA-yyO-2tZma5mD-SAFlKg63HHSc"

headers = {
  # "apikey": "wXXXXXX.."
  "apikey": "wr4DkR1tK5Klzvnsh61PWAVuxM8SxmSM"
}

TOKEN_TRANSLATE = "wr4DkR1tK5Klzvnsh61PWAVuxM8SxmSM"

default_tickers = ['RUB', 'USD', 'EUR', 'BTC', 'CNY', 'INR', 'CHF', 'GBP']
# default_tickers = ['SBD', 'VEF', 'EUR', 'BTC', 'CNY', 'XAG', 'CHF', 'GBP']

help_message = "Обмен валюты.\n" \
               "Доступные команды:\n" \
               "/help - Данное описание\n" \
               "/convert - Конвертер валют\n" \
               "/default - Список валют по умолчанию\n" \
               "/list - Список доступных валют и их коды\n" \
               "/change - Изменить последние 4 валюты\n" \
               " ( Пример: /change AED BYR IRR KGS )\n" \
               " Начало работы:\n" \
               "Нажимаете /convert, вводите сумму для конвертации, нажимаете 'Enter'," \
               " выбираете валюту в которой указали сумму, после выбираете валюту в которую надо конвертировать"


# help_message = text(
#     "Обмен валюты.",
#     "Доступные команды:\n",
#     "/help - Данное описание",
#     "/convert - Конвертер валют",
#     "/default - Список валют по умолчанию",
#     "/list - Список доступных валют и их коды",
#     "/change - Изменить последние 4 валюты \n\t( Пример: /change AED BYR IRR KGS )",
#     "\n Начало работы:",
#     "Нажимаете /convert, вводите сумму для конвертации,"
#     " нажимаете 'Enter', выбираете валюту в которой указали сумму,"
#     " после выбираете валюту в которую надо конвертировать \n",
#     sep="\n"
# )

help_start = "Бот обменного курса валют.\n" \
             " Нажимаете /convert, вводите сумму для конвертации,\n" \
             " нажимаете 'Enter', выбираете валюту в которой указали сумму,\n" \
             " после выбираете валюту в которую надо конвертировать \n" \
             "/help - Описание\n" \
             "/convert - Конвертер валют"

# help_start = text(
#     "Бот обменного курса валют.",
#     "Нажимаете /convert, вводите сумму для конвертации,"
#     " нажимаете 'Enter', выбираете валюту в которой указали сумму,"
#     " после выбираете валюту в которую надо конвертировать \n",
#     "/help - Описание",
#     "/convert - Конвертер валют",
#     sep="\n"
# )
exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}

# ------------------------------------------------------------------
# help - Описание
# convert - Конвертер валют
# default - Список валют по умолчанию
# list - Список доступных валют и их коды
# change - Изменить последние 4 валюты
# (/change AED BYR IRR KGS)
# ---------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------

# -------- https://www.cryptocompare.com/cryptopian/api-keys -------------
# TOKEN_EXC = "81c595854ca4e70e613249d1f2c2af7e96a020627addfba65fb4e3b5a21a811e"
# ---------------------------------------------
# https://translate.googleapis.com/translate_a/t?anno=3&client=te_lib&format=html&v=1.0&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&logld=vTE_20230226&sl=en&tl=ru&tc=1&sr=1&tk=80795.403415&mode=1
# key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&logld=vTE_20230226