import os
import redis

local_launch = False
# local_launch = True

if local_launch:   # secrets from my_config (not included in the repository)
    from my_config import TOKEN_TG, header_apikey, TOKEN_TRANSLATE
    TOKEN_TG = TOKEN_TG
    header_api = {"apikey": header_apikey}  # header apikey for convert
    my_redis = redis.Redis(host='127.0.0.1', port=6379)
    TOKEN_TRANSLATE = TOKEN_TRANSLATE
else:
    TOKEN_TG = os.environ['TOKEN_TG']
    header_api = {"apikey": os.environ["apikey"]}
    my_redis = redis.Redis(host=os.environ['redis_host'],
                           port=10181,
                           password=os.environ['redis_password'])


# Список тикеров отображаемых по умолчанию.
default_tickers = ('RUB', 'USD', 'EUR', 'BTC', 'CNY', 'INR', 'CHF', 'GBP')

url_list = "https://marat2010.ru/exch/"
url_symbols = "https://api.apilayer.com/exchangerates_data/symbols"
url_convert = "https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}"

url_translate = "https://api.apilayer.com/language_translation/translate?target=ru"

help_message = "  Обмен валюты.\n" \
               "Доступные команды:\n" \
               "/help - Данное описание\n" \
               "/convert - Конвертер валют\n" \
               "/default - Сброс списка валют <по умолчанию>\n" \
               "/list - Список доступных валют и их коды\n" \
               "/change - Изменить последние 4 валюты\n" \
               " ( Пример: /change AED BYR IRR KGS )\n" \
               "  Три способа работы:\n" \
               "1. Нажимаете /convert, вводите сумму для конвертации, нажимаете 'Enter'," \
               " выбираете валюту в которой указали сумму, после выбираете валюту в которую надо конвертировать\n" \
               "2. После вывода результатов, можно выбрать одну из указанных значений" \
               " для ее конвертации в другую валюту, чтобы повторно не вводить данные.\n " \
               "3. В строке ввода: 'сумма' 'в чем' 'во что конвертировать'.\n " \
               "Примеры:\n 950 usd EUR \n 1250.55 аргентин датск"

help_start = "Бот обменного курса валют.\n" \
             " Нажимаете /convert, вводите сумму для конвертации,\n" \
             " нажимаете 'Enter', выбираете валюту в которой указали сумму,\n" \
             " после выбираете валюту в которую надо конвертировать \n" \
             "/help - Описание\n" \
             "/convert - Конвертер валют"


# # --------------- Для BotFather, Ввод команд --------------------------
# help - Описание
# convert - Конвертер валют
# default - Список валют по умолчанию
# list - Список доступных валют и их коды
# change - Изменить последние 4 валюты (пример: /change AED BYR IRR KGS)
# # ---------------------------------------------------------------------
