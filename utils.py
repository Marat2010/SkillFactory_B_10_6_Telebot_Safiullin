import requests
from aiogram.utils import json
from config import headers, default_tickers
from config import my_redis as red
# import ujson
# import translators as ts
# import translators.server as tss

url_symbols = "https://api.apilayer.com/exchangerates_data/symbols"
url_translate = "https://api.apilayer.com/language_translation/translate?target=ru"
# url_convert = "https://api.apilayer.com/exchangerates_data/convert?to={RUB}&from={EUR}&amount={300}"
url_convert = "https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}"


class ConvertException(Exception):
    pass


class Chat:
    @staticmethod
    def get_chat_data(chat_id: int) -> dict:
        chat_id = "chat_id_" + str(chat_id)  # Вид ключа ('chat_id_241462113')
        if not red.keys(chat_id):
            return {}
        data = json.loads(red.get(chat_id))
        return data

    @staticmethod
    def set_chat_data(chat_id: int, data: dict) -> dict:
        settings = Chat.get_chat_data(chat_id)

        chat_id = "chat_id_" + str(chat_id)
        settings.update(data)  # Обновление данных
        if data.get('kb_currency'):
            settings['kb_currency'] = str(data['kb_currency'])

        red.set(chat_id, json.dumps(settings))
        return settings


class Convertor:

    @staticmethod
    def get_currencies(tickers: tuple = default_tickers) -> dict:
        """
        Получение словаря отображаемых валют (8 штук) в зависимости от списка тикеров.
        {"RUB": "Российский Рубль", "USD": "Доллар Сша",..}
        """

        with open('symbols_rus.json', 'r') as f_curr:
            all_currencies = json.load(f_curr)

        currencies = {t: all_currencies[t] for t in tickers}
        return currencies

    @staticmethod
    def update_tickers(chat_id: int, tickers):
        with open('symbols_rus.json', 'r') as f_tickers:
            all_currencies = json.load(f_tickers)

        chat_tickers = list(Chat.get_chat_data(chat_id)['tickers'])
        change_tic = [t.upper() for t in tickers[1:5]]  # ['/change', 'AED', 'KGS', 'IRR', 'KGS']
        tickers = [t for t in change_tic if (t in all_currencies.keys()) and (t not in chat_tickers)]

        chat_tickers = chat_tickers[:len(chat_tickers)-len(tickers)]
        chat_tickers.extend(tickers)
        chat_tickers = tuple(chat_tickers)

        return chat_tickers, tickers

    @staticmethod
    def get_price(amount, from_ticker, to_ticker):
        url_price = url_convert.format(to_ticker, from_ticker, amount)
        response = requests.request("GET", url_price, headers=headers)
        status_code = response.status_code

        if status_code != 200:
            raise ConvertException(f"API конвертор: плохой ответ ( не {status_code} !!!)")
        try:
            price = json.loads(response.content)
        except KeyError as e:
            raise ConvertException(f"API конвертор: не может получить цены валют ({e})")

        return price['result']

    @staticmethod
    def get_symbols() -> dict:
        """
        Получение всех валют: тикеров и названия на англ.
        """
        response = requests.request("GET", url_symbols, headers=headers)
        status_code = response.status_code
        if status_code != 200:
            raise ConvertException(f"API конвертор: плохой ответ ( не {status_code} !!!)")
        try:
            symbols = json.loads(response.content)['symbols']
        except KeyError as e:
            raise ConvertException(f"API конвертор: не может получить список валют ({e})")

        with open('symbols.json', 'w', encoding='utf-8') as f:
            json.dump(symbols, f, indent=4, ensure_ascii=False)

        return symbols

# ------------------------------------
# def digit_check(s: str) -> str:
#     try:
#         float(s)
#         print("===1===")
#     except ValueError:
#         print("===2===")
#         return f"= NO FLOAT =: {s}"
#
#     try:
#         int(s)
#         s = f"{int(s): _}"
#         print("===3===")
#     except ValueError:
#         s = f"{float(s): _.2f}"
#         print("===4===")
#         return s
#
#     return s
# ------------------------------------


def digit_check(s: str) -> tuple:
    n = False
    s_out = False
    if s.replace('_', '').replace('.', '', 1).isdigit():
        try:
            n = int(s)
            s_out = f"{int(s):_}"
        except ValueError:
            n = float(s)
            dot = s.split('.')  # Отдельная обработка целой и вещ. части
            s_out = f"{int(dot[0]):_}"

            s_out += '.' + dot[1]
            # if len(dot[1]) > 4:
            if len(dot[1]) == 5:
                s_out += " - Совсем с ума .. 🤪, копейки вводить 😂😂😂  "

    print(f"==DIGIT=={n}==, =={s_out}==")
    return n, s_out


# ________________________________________________________
    # Использовался ранее, для перевода названия валют.
    # @staticmethod
    # def translate(text):
    #     from_language, to_language = 'en', 'ru'
    #     result = tss.google(text, from_language, to_language)
    #     return result
# ________________________________________________________


if __name__ == '__main__':
    pass
    # amount = 300
    # from_ticker = 'RUB'
    # to_ticker = 'USD'
    #
    # rez = Convertor.get_price(amount, from_ticker, to_ticker)
    # print("rez:", rez)  # rez: {
    #                             # 'success': True,
    #                             # 'query': {'from': 'RUB', 'to': 'USD', 'amount': 300},
    #                             # 'info': {'timestamp': 1678413783, 'rate': 0.013184},
    #                             # 'date': '2023-03-10',
    #                             # 'result': 3.9552
    #                             # }


# _____________________________________________________________
    # def get_price(base, sym, amount):

# _____________________________________________________________
# https://apilayer.com/marketplace/exchangerates_data-api?_gl=1*3mtuzh*_ga*MTA5NDQ3NzY4Ny4xNjc3NTM0Njg0*_ga_HGV43FGGVM*MTY3NzUzNDY4NC4xLjEuMTY3NzUzNDY5MS41My4wLjA.%3Fe=Sign+In&l=Success?e=Sign+In&l=Success
# # _____________________________________________________________
# import requests
#
# url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=300"
#
# payload = {}
# headers= {
#   "apikey": "wr4DkR1tK5Klzvnsh61PWAVuxM8SxmSM"
# }
#
# response = requests.request("GET", url, headers=headers, data = payload)
#
# status_code = response.status_code
# result = response.text
#
# ---------result------------
# {
#   "date": "2023-03-10",
#   "info": {
#     "rate": 80.363442,
#     "timestamp": 1678412522
#   },
#   "query": {
#     "amount": 300,
#     "from": "EUR",
#     "to": "RUB"
#   },
#   "result": 24109.0326,
#   "success": true
# }

# _____________________________________________________________
# _____________________________________________________________
# s_out = f"{float(s):_.2f}"
# _____________________________________________________________
    # r = Convertor().get_default_currencies()
    # print("===R==", r)

    # with open('symbols.json', 'r') as f:
    #     curr = ujson.load(f)
    #
    # print("==CUR== ", type(curr), "== ", curr)
    #
    # curr_lst = [*curr]
    # print(type(curr_lst), "==<>=", curr_lst)
    # rez = Convertor.get_default_currencies(curr_lst[0:10])
    # print("== ", type(rez), "--== ", rez)
# _____________________________________________________________
    # def __init__(self):
    #     self.input_str = ''
    #     self.old_input_str = ''
    #     self.default_currencies = {}  # Словарь отображаемых валют {"RUB": "Российский Рубль", "USD": "Доллар Сша",..}
    #     self.tickers = default_tickers  # Тикеры ['RUB', 'USD',..]
    #     # self.de   fault_currencies = self.get_default_currencies()  # Словарь отображаемых валют на русском

# _____________________________________________________________
# for k in data:  # Обновление данных
#     settings[k] = data[k]  # Необходимо перевести в строку для Redis
# settings = {t: data[t] for t in data}

# _____________________________________________________________
# currencies = {}
# for t in tickers:
#     currencies[t] = all_currencies[t]
# _____________________________________________________________
# # settings.update(data)  # Обновление данных
# _____________________________________________________________
# input_str = red.hget(chat_id, 'input_str').decode("utf-8")
# old_input_str = red.hget(chat_id, 'old_input_str').decode("utf-8")
# tickers = red.hget(chat_id, 'tickers').decode("utf-8")
# currencies = red.hget(chat_id, 'currencies').decode("utf-8")
# kb_currency = red.hget(chat_id, 'kb_currency').decode("utf-8")
#
# data = {
#     'input_str': input_str,
#     'old_input_str': old_input_str,
#     'tickers': tickers,
#     'currencies': currencies,
#     'kb_currency': kb_currency
# }

# Второй способ загрузки и выгрузки через Json:
# red.set(chat_id, json.dumps(data))
# ----------------------
# data = red.hset(chat_id, mapping=settings)

# Второй способ загрузки и выгрузки через Json:
# red.set(chat_id, json.dumps(settings))
# settings = json.loads(red.get(chat_id))
# _____________________________________________________________
# _____________________________________________________________
#     @staticmethod  # Old get_default_currencies
#     def get_default_currencies(currencies=default_currencies):
#         cur = Convertor.get_symbols()
#         cur_lst = [cur[i] for i in currencies]
#         text_cur = ', '.join(cur_lst)
#
#         print('====text_cur==', text_cur)
#         translate_text = Convertor.translate(text_cur)
#
#         translate_list = translate_text.split(', ')
#         print('====translate_list==', translate_list)
#
#         russ_dict = {}
#         for i, n in enumerate(currencies):
#             russ_dict[n] = translate_list[i]
#
#         # with open('symbols_rus.json', 'w')as f:
#         with open('symbols_rus.json', 'w', encoding='utf-8')as f:
#             ujson.dump(russ_dict, f, indent=4, ensure_ascii=False)
#         return russ_dict
# _____________________________________________________________
# print(f"==SELF.Tick: {self.tickers} = TICKERS_ADD= {tickers}")

# --------------------------------------
# переводчик yandex:
# trnsl.1.1.20190928T185613Z.4d1d79f81bf497a8.75037b63bf025f65040895814428eadc0438f8a4
# y0_AgAAAAAZ6ZusAATuwQAAAADdPo09OomlTIczQtiWIzErogrfsWFeWxs
# russ_dict[n] = {translate_list[i] for i, n in enumerate(default_currencies)}
# ------------------------------------------------------
# {
#  "iamToken": "t1.9euelZrOi8fMnZ6az5uUk5fIz52Pxu3rnpWalJKSnMqdzo6el4nOyIrMmIzl8_dbWw9g-e8Gdi5m_t3z9xsKDWD57wZ2Lmb-.gPf3so4McXjI8zuzxpTwpeekiHVMQWZUooXpEb2ChP0wbnuAsIKruny4JIbc2IjlHoXSnFDmVnPt5jYci8UbDQ",
#  "expiresAt": "2023-02-27T14:15:00.322192633Z"
# }
# ------------------------------------------------------
# Использование IAM-токена, полученного с помощью CLI
# export IAM_TOKEN=`yc iam create-token`
# curl -H "Authorization: Bearer ${IAM_TOKEN}" \
#   https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds

# Authorization: Bearer <IAM-токен>

# --------------------------------------
    # rez = Convertor.get_default_currencies(curr_lst)
    # rez = Convertor.get_default_currencies()
# --------------------------------------
# --------------------------------------
# --------------------------------------
# result = tss.alibaba(text, professional_field='general')
# result = tss.alibaba(text, from_language, to_language)
# print('=== Trans google==', result)
# ------------------------------------------------------
# import requests
#
# url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=300"
#
# payload = {}
# headers= {
#   "apikey": "wr4DkR1tK5Klzvnsh61PWAVuxM8SxmSM"
# }
#
# response = requests.request("GET", url, headers=headers, data=payload)
#
# status_code = response.status_code
# result = response.text
#
# print("--1--:", result)
# print("--2--:", payload)
# ------------------------------------------------------
# {
#     "success": true,
#     "query": {
#         "from": "EUR",
#         "to": "RUB",
#         "amount": 300
#     },
#     "info": {
#         "timestamp": 1677538563,
#         "rate": 79.473818
#     },
#     "date": "2023-02-27",
#     "result": 23842.1454
# }
# ------------------------------------------------------
        # check input language with language_map
        # assert from_language in tss._google.language_map  # request once first, then

        # payload = text.encode("utf-8")
        # # payload = text.encode()
        # payload = text
        # print("====payload==== ", payload)
        # response = requests.request("POST", url_translate, headers=headers, data=payload)
        # status_code = response.status_code
        # print("wwwwww--payload===", payload)
        # print("wwwwww--status_code===", status_code)
        # print("wwwwww--response.content===", response.content)
        # result = ujson.loads(response.content)['translations'][0]['translation']


    # def translate(text):
    #     # payload = text.encode("utf-8")
    #     # payload = text.encode()
    #     payload = text
    #     print("====payload==== ", payload)
    #     response = requests.request("POST", url_translate, headers=headers, data=payload)
    #     status_code = response.status_code
    #     print("wwwwww--payload===", payload)
    #     print("wwwwww--status_code===", status_code)
    #     print("wwwwww--response.content===", response.content)
    #     result = ujson.loads(response.content)['translations'][0]['translation']
    #     return result

# ------------------------------------------------------
# url = "https://api.apilayer.com/exchangerates_data/symbols"
# Результат:
# all_symbols = {
#     "success": true,
#     "symbols": {
#         "AED": "United Arab Emirates Dirham",
#         "AFN": "Afghan Afghani",
#         "ALL": "Albanian Lek",
#         "AMD": "Armenian Dram",
#         "ANG": "Netherlands Antillean Guilder",
#         "AOA": "Angolan Kwanza",
#         "ARS": "Argentine Peso",
#         "AUD": "Australian Dollar",
#         "AWG": "Aruban Florin",
#         "AZN": "Azerbaijani Manat",
#         "BAM": "Bosnia-Herzegovina Convertible Mark",
#         "BBD": "Barbadian Dollar",
#         "BDT": "Bangladeshi Taka",
#         "BGN": "Bulgarian Lev",
#         "BHD": "Bahraini Dinar",
#         "BIF": "Burundian Franc",
#         "BMD": "Bermudan Dollar",
#         "BND": "Brunei Dollar",
#         "BOB": "Bolivian Boliviano",
#         "BRL": "Brazilian Real",
#         "BSD": "Bahamian Dollar",
#         "BTC": "Bitcoin",
#         "BTN": "Bhutanese Ngultrum",
#         "BWP": "Botswanan Pula",
#         "BYN": "New Belarusian Ruble",
#         "BYR": "Belarusian Ruble",
#         "BZD": "Belize Dollar",
#         "CAD": "Canadian Dollar",
#         "CDF": "Congolese Franc",
#         "CHF": "Swiss Franc",
#         "CLF": "Chilean Unit of Account (UF)",
#         "CLP": "Chilean Peso",
#         "CNY": "Chinese Yuan",
#         "COP": "Colombian Peso",
#         "CRC": "Costa Rican Col\u00f3n",
#         "CUC": "Cuban Convertible Peso",
#         "CUP": "Cuban Peso",
#         "CVE": "Cape Verdean Escudo",
#         "CZK": "Czech Republic Koruna",
#         "DJF": "Djiboutian Franc",
#         "DKK": "Danish Krone",
#         "DOP": "Dominican Peso",
#         "DZD": "Algerian Dinar",
#         "EGP": "Egyptian Pound",
#         "ERN": "Eritrean Nakfa",
#         "ETB": "Ethiopian Birr",
#         "EUR": "Euro",
#         "FJD": "Fijian Dollar",
#         "FKP": "Falkland Islands Pound",
#         "GBP": "British Pound Sterling",
#         "GEL": "Georgian Lari",
#         "GGP": "Guernsey Pound",
#         "GHS": "Ghanaian Cedi",
#         "GIP": "Gibraltar Pound",
#         "GMD": "Gambian Dalasi",
#         "GNF": "Guinean Franc",
#         "GTQ": "Guatemalan Quetzal",
#         "GYD": "Guyanaese Dollar",
#         "HKD": "Hong Kong Dollar",
#         "HNL": "Honduran Lempira",
#         "HRK": "Croatian Kuna",
#         "HTG": "Haitian Gourde",
#         "HUF": "Hungarian Forint",
#         "IDR": "Indonesian Rupiah",
#         "ILS": "Israeli New Sheqel",
#         "IMP": "Manx pound",
#         "INR": "Indian Rupee",
#         "IQD": "Iraqi Dinar",
#         "IRR": "Iranian Rial",
#         "ISK": "Icelandic Kr\u00f3na",
#         "JEP": "Jersey Pound",
#         "JMD": "Jamaican Dollar",
#         "JOD": "Jordanian Dinar",
#         "JPY": "Japanese Yen",
#         "KES": "Kenyan Shilling",
#         "KGS": "Kyrgystani Som",
#         "KHR": "Cambodian Riel",
#         "KMF": "Comorian Franc",
#         "KPW": "North Korean Won",
#         "KRW": "South Korean Won",
#         "KWD": "Kuwaiti Dinar",
#         "KYD": "Cayman Islands Dollar",
#         "KZT": "Kazakhstani Tenge",
#         "LAK": "Laotian Kip",
#         "LBP": "Lebanese Pound",
#         "LKR": "Sri Lankan Rupee",
#         "LRD": "Liberian Dollar",
#         "LSL": "Lesotho Loti",
#         "LTL": "Lithuanian Litas",
#         "LVL": "Latvian Lats",
#         "LYD": "Libyan Dinar",
#         "MAD": "Moroccan Dirham",
#         "MDL": "Moldovan Leu",
#         "MGA": "Malagasy Ariary",
#         "MKD": "Macedonian Denar",
#         "MMK": "Myanma Kyat",
#         "MNT": "Mongolian Tugrik",
#         "MOP": "Macanese Pataca",
#         "MRO": "Mauritanian Ouguiya",
#         "MUR": "Mauritian Rupee",
#         "MVR": "Maldivian Rufiyaa",
#         "MWK": "Malawian Kwacha",
#         "MXN": "Mexican Peso",
#         "MYR": "Malaysian Ringgit",
#         "MZN": "Mozambican Metical",
#         "NAD": "Namibian Dollar",
#         "NGN": "Nigerian Naira",
#         "NIO": "Nicaraguan C\u00f3rdoba",
#         "NOK": "Norwegian Krone",
#         "NPR": "Nepalese Rupee",
#         "NZD": "New Zealand Dollar",
#         "OMR": "Omani Rial",
#         "PAB": "Panamanian Balboa",
#         "PEN": "Peruvian Nuevo Sol",
#         "PGK": "Papua New Guinean Kina",
#         "PHP": "Philippine Peso",
#         "PKR": "Pakistani Rupee",
#         "PLN": "Polish Zloty",
#         "PYG": "Paraguayan Guarani",
#         "QAR": "Qatari Rial",
#         "RON": "Romanian Leu",
#         "RSD": "Serbian Dinar",
#         "RUB": "Russian Ruble",
#         "RWF": "Rwandan Franc",
#         "SAR": "Saudi Riyal",
#         "SBD": "Solomon Islands Dollar",
#         "SCR": "Seychellois Rupee",
#         "SDG": "Sudanese Pound",
#         "SEK": "Swedish Krona",
#         "SGD": "Singapore Dollar",
#         "SHP": "Saint Helena Pound",
#         "SLE": "Sierra Leonean Leone",
#         "SLL": "Sierra Leonean Leone",
#         "SOS": "Somali Shilling",
#         "SRD": "Surinamese Dollar",
#         "STD": "S\u00e3o Tom\u00e9 and Pr\u00edncipe Dobra",
#         "SVC": "Salvadoran Col\u00f3n",
#         "SYP": "Syrian Pound",
#         "SZL": "Swazi Lilangeni",
#         "THB": "Thai Baht",
#         "TJS": "Tajikistani Somoni",
#         "TMT": "Turkmenistani Manat",
#         "TND": "Tunisian Dinar",
#         "TOP": "Tongan Pa\u02bbanga",
#         "TRY": "Turkish Lira",
#         "TTD": "Trinidad and Tobago Dollar",
#         "TWD": "New Taiwan Dollar",
#         "TZS": "Tanzanian Shilling",
#         "UAH": "Ukrainian Hryvnia",
#         "UGX": "Ugandan Shilling",
#         "USD": "United States Dollar",
#         "UYU": "Uruguayan Peso",
#         "UZS": "Uzbekistan Som",
#         "VEF": "Venezuelan Bol\u00edvar Fuerte",
#         "VES": "Sovereign Bolivar",
#         "VND": "Vietnamese Dong",
#         "VUV": "Vanuatu Vatu",
#         "WST": "Samoan Tala",
#         "XAF": "CFA Franc BEAC",
#         "XAG": "Silver (troy ounce)",
#         "XAU": "Gold (troy ounce)",
#         "XCD": "East Caribbean Dollar",
#         "XDR": "Special Drawing Rights",
#         "XOF": "CFA Franc BCEAO",
#         "XPF": "CFP Franc",
#         "YER": "Yemeni Rial",
#         "ZAR": "South African Rand",
#         "ZMK": "Zambian Kwacha (pre-2013)",
#         "ZMW": "Zambian Kwacha",
#         "ZWL": "Zimbabwean Dollar"
#     }
# }

# ------------------------------------
# "символы": {
# "AED": "Дирхам ОАЭ",
# "AFN": "Афганский афгани",
# "ALL": "Албанский лек",
# "AMD": "Армянский Драм",
# "ANG": "Нидерландский антильский гульден",
# "AOA": "Ангольская кванза",
# "ARS": "Аргентинское песо",
# "AUD": "Австралийский доллар",
# "AWG": "Арубанский Флорин",
# "AZN": "Азербайджанский манат",
# "BAM": "Конвертируемая марка Боснии и Герцеговины",
# "BBD": "барбадосский доллар",
# "BDT": "Бангладешская така",
# "BGN": "Болгарский Лев",
# "BHD": "бахрейнский динар",
# "BIF": "Бурундийский франк",
# "BMD": "Бермудский доллар",
# "BND": "Брунейский доллар",
# "BOB": "Боливийский Боливиано",
# "BRL": "бразильский реал",
# "BSD": "Багамский доллар",
# "BTC": "Биткойн",
# "BTN": "Бутанский нгултрум",
# "BWP": "Ботсванская пула",
# "BYN": "Новый белорусский рубль",
# "BYR": "Белорусский рубль",
# "BZD": "Белизский доллар",
# "CAD": "Канадский доллар",
# "CDF": "Конголезский франк",
# "CHF": "Швейцарский франк",
# "CLF": "Чилийская расчетная единица (UF)",
# "CLP": "Чилийское песо",
# "CNY": "китайский юань",
# "COP": "Колумбийское песо",
# "CRC": "Коста-риканский столбец",
# "CUC": "Кубинское конвертируемое песо",
# "ЧАШКА": "Кубинское песо",
# "CVE": "Эскудо Кабо-Верде",
# "CZK": "Чешская крона",
# "DJF": "Джибутийский франк",
# "DKK": "Датская крона",
# "DOP": "Доминиканский песо",
# "DZD": "Алжирский динар",
# "EGP": "Египетский фунт",
# "ERN": "Эритрейская накфа",
# "ETB": "Эфиопский быр",
# "ЕВРО": "Евро",
# "FJD": "фиджийский доллар",
# "FKP": "Фунт Фолклендских островов",
# "GBP": "Британский фунт стерлингов",
# "GEL": "Грузинский лари",
# "GGP": "Фунт Гернси",
# "GHS": "Ганский седи",
# "GIP": "Гибралтарский фунт",
# "GMD": "гамбийский даласи",
# "GNF": "Гвинейский франк",
# "GTQ": "Гватемальский кетсаль",
# "GYD": "Гайанский доллар",
# "HKD": "Гонконгский доллар",
# "HNL": "гондурасская лемпира",
# "HRK": "Хорватская куна",
# "HTG": "Гаитянский гурд",
# "HUF": "Венгерский форинт",
# "IDR": "Индонезийская рупия",
# "ILS": "Новый израильский шекель",
# "IMP": "Мэнский фунт",
# "INR": "Индийская рупия",
# "IQD": "Иракский динар",
# "IRR": "Иранский риал",
# "ISK": "Исландский Kr\u00f3na",
# "JEP": "Джерсийский фунт",
# "JMD": "Ямайский доллар",
# "JOD": "Иорданский динар",
# "JPY": "Японская иена",
# "KES": "Кенийский шиллинг",
# "KGS": "Кыргызский сом",
# "KHR": "камбоджийский риель",
# "KMF": "Коморский франк",
# "KPW": "Северокорейская вона",
# "KRW": "Южнокорейский вон",
# "KWD": "Кувейтский динар",
# "KYD": "Доллар Каймановых островов",
# "KZT": "Казахстанский тенге",
# "LAK": "лаосский кип",
# "LBP": "ливанский фунт",
# "LKR": "Шри-ланкийская рупия",
# "LRD": "либерийский доллар",
# "LSL": "Лесото Лоти",
# "LTL": "Литовские литы",
# "LVL": "Латвийские латы",
# "LYD": "ливийский динар",
# "MAD": "Марокканский дирхам",
# "MDL": "Молдавский лей",
# "MGA": "Малагасийский Ариари",
# "МКД": "Македонский денар",
# "ММК": "Мьянма Кьят",
# "MNT": "монгольский тугрик",
# "MOP": "Маканесская патака",
# "MRO": "мавританская угия",
# "MUR": "маврикийская рупия",
# "MVR": "Мальдивская руфия",
# "MWK": "малавийская квача",
# "MXN": "Мексиканское песо",
# "MYR": "Малайзийский ринггит",
# "МЗН": "Мозамбикский метикал",
# "NAD": "Доллар Намибии",
# "NGN": "Нигерийская Найра",
# "NIO": "Никарагуанская кардоба",
# "NOK": "норвежская крона",
# "NPR": "Непальская рупия",
# "NZD": "Доллар Новой Зеландии",
# "OMR": "Оманский риал",
# "PAB": "панамский бальбоа",
# "PEN": "Перуанский Нуэво Соль",
# "PGK": "Кина Папуа-Новой Гвинеи",
# "PHP": "Филиппинское песо",
# "PKR": "Пакистанская рупия",
# "PLN": "Польские злотые",
# "PYG": "парагвайский гуарани",
# "QAR": "Катарский риал",
# "RON": "румынский лей",
# "RSD": "сербский динар",
# "RUB": "Российский рубль",
# "RWF": "Руандийский франк",
# "SAR": "Саудовский риал",
# "SBD": "Доллар Соломоновых Островов",
# "SCR": "Сейшельская рупия",
# "SDG": "Суданский фунт",
# "SEK": "Шведская крона",
# "SGD": "Сингапурский доллар",
# "SHP": "Фунт Святой Елены",
# "СКВ": "Сьерра-Леонеан Леоне",
# "SLL": "Сьерра-Леонеан Леоне",
# "SOS": "Сомалийский шиллинг",
# "SRD": "Суринамский доллар",
# -----------------
# 'São Tomé and Príncipe Dobra'
# Сан-Томе и Принсипи Добра
# Добра Сан-Томе и Принсипи
# Это Том и Пренсипи Добра
# -----------------
# "STD": "Добра Сан-Томе и Принсипи"
# "SVC": "Сальвадорский столб"
# "SYP": "Сирийский фунт"
# "SZL": "Свазиленд"
# "THB": "Тайский бат"
# "TJS": "Таджикистанские сомони",
# "ТМТ": "Туркменский манат",
# "TND": "Тунисский динар"
# "TOP": "Тонганское пространство",
# "TRY": "Турецкая лира"
# "TTD": "Доллар Тринидада и Тобаго"
# "TWD": "Новый тайваньский доллар"
# "TZS": "Танзанийский шиллинг"
# "UAH": "Украинская гривна"
# "UGX": "Угандийский шиллинг",
# "USD": "Доллар США"
# "UYU": "Уругвайское песо",
# "UZS": "Узбекский сом"
# "ВЭФ": "Венесуэла футбол сильный"
# "ВЕСЬ": "Государь Боливар"
# "VND": "Вьетнамский донг"
# "ВУВ": "Люди Люди",
# "WST": "Западное Самоа",
# "XAF": "Франк CFA BEAC"
# "XAG": "Серебро (тройская унция)",
# "XAU": "Золото (тройская унция)"
# "XCD": "Восточно-карибский доллар"
# "XDR": "Специальные права заимствования",
# "XOF": "Франки КФА"
# "XPF": "Франки CFP"
# "YER": "Йеменский реал",
# "ZAR": "южноафриканский ранд"
# "ЗМК": "Замбийская квача (до 2013 г.)",
# "ZMW": "Замбия Квача",
# "ZWL": "Зимбабвийский доллар"

