#Импортируем необходимые библиотеки
import requests
import json
#Импорт валют из файла config.py
from config import values

#Собственный класс исключений
class APIException(Exception):
    pass

#Класс бота теллеграмм 
class TelebotConverter:
    #Ф-ия получения курса валют и умножения на количество
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        try:
            quote_ticker = values[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = values[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты.')

        try:
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
            total_base = float(json.loads(r.content)[values[base]])
        except Exception:
            raise APIException(f'Не удалось обработать запрос курса валют.')

        return total_base * amount
