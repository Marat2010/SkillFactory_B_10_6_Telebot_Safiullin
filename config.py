# TOKEN_TG = "1444339635:XXXXX-.."
# TOKEN_TG = "1444339635:AAEWaQQmfy-Guk47iioxwIDiT7lbL5h5z-I"
import redis
import os

# # ------ Для alwaysdata --------------------
# TOKEN_TG = os.environ['TOKEN_TG']
# headers = {"apikey": os.environ["apikey"]}
#
# red = redis.Redis(
#     host=os.environ['redis_host'],
#     port=10181,
#     password=os.environ['redis_password']
# )
# --------------
# red = redis.Redis(
#     host='redis-10181.c250.eu-central-1-1.ec2.cloud.redislabs.com',
#     port=10181,
#     password='HuVRdjl0mauP6yBJvhJDsZGBa4KdQYDo'
# )
# ---------------------

# TOKEN_TG_ser = "6065866125:AAHTL1GJA-yyO-2tZma5mD-SAFlKg63HHSc"
TOKEN_TG = "6189775277:AAEMeeJKvor6PUbywS1UV76cqjWLQbPe0T4"

headers = {
  # "apikey": "wXXXXXX.."
  "apikey": "wr4DkR1tK5Klzvnsh61PWAVuxM8SxmSM"
}

TOKEN_TRANSLATE = "xxxxx"

my_redis = redis.Redis(
    host='127.0.0.1',
    port=6379
)


# Список тикеров отображаемых по умолчанию.
default_tickers = ('RUB', 'USD', 'EUR', 'BTC', 'CNY', 'INR', 'CHF', 'GBP')

# url_list = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_" \
#            "%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D1%83%D1%8E%D1%89%D0%B8%D1%85_" \
#            "%D0%B2%D0%B0%D0%BB%D1%8E%D1%82"

# url_list = "https://marat2010.github.io/SkillFactory_module_A3_Safiullin/bot.html"

url_list = "https://marat2010.ru/exch/"

help_message = "  Обмен валюты.\n" \
               "Доступные команды:\n" \
               "/help - Данное описание\n" \
               "/convert - Конвертер валют\n" \
               "/default - Сброс списка валют <по умолчанию>\n" \
               "/list - Список доступных валют и их коды\n" \
               "/change - Изменить последние 4 валюты\n" \
               " ( Пример: /change AED BYR IRR KGS )\n" \
               " Начало работы:\n" \
               "Нажимаете /convert, вводите сумму для конвертации, нажимаете 'Enter'," \
               " выбираете валюту в которой указали сумму, после выбираете валюту в которую надо конвертировать"

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
# # change AED BYR IRR KGS - Изменить последние 4 валюты
# # ---------------------------------------------------------------------
