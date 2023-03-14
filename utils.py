import requests
from aiogram.utils import json
from config import header_api, default_tickers
from config import my_redis as red
from config import url_symbols, url_convert, url_translate
import re
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
    def update_chat_data(chat_id: int, data: dict) -> dict:
        settings = Chat.get_chat_data(chat_id)

        chat_id = "chat_id_" + str(chat_id)
        settings.update(data)  # Обновление данных
        if data.get('kb_currency'):
            settings['kb_currency'] = str(data['kb_currency'])

        red.set(chat_id, json.dumps(settings))
        return settings


class Convertor:

    @staticmethod
    def get_all_currencies() -> dict:
        """
        Получение словаря всех валют.
        {"AED": "Дирхам ОАЭ", "AFN": "Афганский афгани", ..}
        """
        if not red.get('all_currencies'):
            with open('symbols_rus.json', 'r') as f_curr:
                all_currencies = json.load(f_curr)
                red.set('all_currencies', json.dumps(all_currencies))
        else:
            all_currencies = json.loads(red.get('all_currencies'))
        return all_currencies

    @staticmethod
    def get_currencies(tickers: tuple = default_tickers) -> dict:
        """
        Получение словаря отображаемых валют (8 штук) в зависимости от списка тикеров.
        {"RUB": "Российский Рубль", "USD": "Доллар Сша",..}
        """
        all_currencies = Convertor.get_all_currencies()
        currencies = {t: all_currencies[t] for t in tickers}
        return currencies

    @staticmethod
    def update_tickers(chat_id: int, tickers) -> tuple:
        """
        Изменение списка тикеров отображаемых валют. Всего 8 штук.
        Максимум можно изменить последние 4.
        Возвращает:
         chat_tickers - новый полный список тикеров
         tickers - новые добавленные тикеры.
        """

        all_currencies = Convertor.get_all_currencies()

        chat_tickers = list(Chat.get_chat_data(chat_id)['tickers'])
        change_tic = [t.upper() for t in tickers[1:5]]  # ['/change', 'AED', 'KGS', 'IRR', 'KGS']
        tickers = [t for t in change_tic if (t in all_currencies.keys()) and (t not in chat_tickers)]

        chat_tickers = chat_tickers[:len(chat_tickers)-len(tickers)]
        chat_tickers.extend(tickers)
        chat_tickers = tuple(chat_tickers)

        # Обновление данных чата
        chat_values = {'tickers': chat_tickers,
                       'currencies': Convertor.get_currencies(chat_tickers),
                       }
        Chat.update_chat_data(chat_id, chat_values)

        return chat_tickers, tickers

    @staticmethod
    def get_price(amount, from_ticker, to_ticker):
        url_price = url_convert.format(to_ticker, from_ticker, amount)
        try:
            response = requests.request("GET", url_price, headers=header_api)
            status_code = response.status_code
        except requests.exceptions.ConnectionError as e:
            raise ConvertException(f"😢 Нет соединения с API конвертора !!!")

        if status_code != 200:
            raise ConvertException(f"😢 API конвертор: плохой ответ !!! ( status_code: {status_code} )")
        try:
            price = json.loads(response.content)
            price = price['result']
        except KeyError as e:
            raise ConvertException(f"😢 API конвертор: не может получить результат. ({e})")

        return price

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


def ticker_check(ticker: str, all_currencies: dict) -> str:
    """
    Проверка и поиск тикеров валют
    """
    tick = all_currencies.get(ticker.upper())

    if tick:
        tick = ticker.upper()
    else:
        for t, c in all_currencies.items():  # (TND, Тунисский динар)
            if re.search(ticker.lower(), c.lower()):
                tick = t.upper()
                return tick  # выходим после первого нахождения
    return tick


def input_str_check(chat_id: int, s: str) -> dict:
    """
    Основная обработка входящей строки
    """

    try:
        num_str, from_ticker, to_ticker = s.split()
    except ValueError:
        sh_input_num = "Неверное количество параметров!!!\n Должно быть число, и две валюты!"
        return {'rez': False, 'converted_text': sh_input_num, 'change_tic': False}

    num, str_out = digit_check(num_str)  # num: число или False, str_out: строка чисел для вывода

    if num:
        sh_input_num = str_out
    else:
        sh_input_num = f"{num_str}  -  Это не число!!!"
        return {'rez': False, 'converted_text': sh_input_num, 'change_tic': False}

    # -------- Проверка тикеров --------
    all_currencies = Convertor.get_all_currencies()

    from_tick = ticker_check(from_ticker, all_currencies)
    to_tick = ticker_check(to_ticker, all_currencies)
    change_tic = False  # Тикеры для замены
    if not from_tick:
        num = False
        converted_text = f"{from_ticker}  - Такой валюты нет!!! 🤪"
    elif not to_tick:
        num = False
        converted_text = f"{to_ticker}  - Такой валюты нет!!! 🤪"
    elif from_tick == to_tick:
        num = False
        converted_text = f" Валюты должны быть разными!!! 🤪"
    else:
        try:
            # converted_sum = 12345.678912  # Для теста, без конвертации.
            converted_sum = Convertor.get_price(num, from_tick, to_tick)
            converted_sum = f"{converted_sum: _.4f}"
        except ConvertException as e:
            converted_sum = f"{e}"

        tickers = ['/change', from_tick, to_tick]
        chat_tickers, change_tic = Convertor.update_tickers(chat_id, tickers)
        result = [sh_input_num, from_tick, converted_sum, to_tick]
        # Обновление данных чата
        settings = Chat.update_chat_data(chat_id, {'result': result})
        currencies = settings.get('currencies')

        converted_text = f"{sh_input_num}  {from_tick} ({currencies[from_tick]})  =" \
                         f"  {converted_sum}  {to_tick} ({currencies[to_tick]})\n"

    return {'rez': num, 'converted_text': converted_text, 'change_tic': change_tic}

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

