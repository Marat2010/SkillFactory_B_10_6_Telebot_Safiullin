import requests
from aiogram.utils import json
from config import header_api, default_tickers
from config import my_redis as red
from config import url_symbols, url_convert, url_translate
import re
# import ujson
# import translators as ts
# import translators.server as tss


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
        response = requests.request("GET", url_price, headers=header_api)
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
        response = requests.request("GET", url_symbols, headers=header_api)
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
            if len(dot[1]) == 5:
                s_out += " - Совсем с ума .. 🤪, копейки вводить 😂😂😂  "

    return n, s_out


def input_str_check(s: str) -> tuple:
    input_str, from_ticker, to_ticker = s.split()

    num, str_out = digit_check(input_str)  # num: число или False, str_out: строка чисел для вывода

    if num:
        sh_input_num = str_out
    else:
        sh_input_num = f"{input_str}  -  Это не число!!!"
        return num, sh_input_num  # Выход, чтобы дальше не считать

    # Проверка тикеров
    # ------------------------------------------
    with open('symbols_rus.json', 'r') as f_curr:
        all_currencies = json.load(f_curr)

    from_tick = all_currencies.get(from_ticker.upper())
    to_tick = all_currencies.get(to_ticker.upper())
    print(f"===Проверка тикеров==: {from_ticker}, {to_ticker}")

    if not from_tick:
        for t, c in all_currencies.items():  # (TND, Тунисский динар)
            if re.match(from_ticker.lower(), c.lower()):
                print("======= from_ticker === ", t, '==', c)
                from_ticker = t.upper()

    if not to_tick:
        for t, c in all_currencies.items():  # (TND, Тунисский динар)
            if re.match(to_ticker.lower(), c.lower()):
                print("======= to_ticker === ", t, '==', c)
                to_ticker = t.upper()

    print(f"======= from_ticker: {from_ticker} ===== to_ticker: {to_ticker} ===")

    # ------------------------------------------

    if from_ticker == to_ticker:
        converted_sum = f" Валюты должны быть разными!!!"
    else:
        converted_sum = 173123.45113
        # converted_sum = Convertor.get_price(num, from_ticker, to_ticker)
        converted_sum = f"{converted_sum: _.2f}"

    return num, sh_input_num, from_ticker, converted_sum, to_ticker


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



