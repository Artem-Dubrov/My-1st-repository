import requests
import json

from config import currency_list,API_key

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base:str, quote:str, amount:float ):

        if quote==base:
            raise APIException(f'Вы указали одинаковую валюту для перевода: *{base}*. Перевод *{base}* в *{quote}* '
                               f'невозможен. Пожалуйста, выберите разные валюты для конвертации.')
        try:
            base_name = currency_list[base]
        except KeyError:
            raise APIException(f'Неверно указана валюта *{base}*')
        try:
            quote_name = currency_list[quote]
        except KeyError:
            raise APIException(f'Неверно указана валюта *{quote}* ')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты *{amount}*')
        r=requests.get(f"https://v6.exchangerate-api.com/v6/{API_key}/latest/{base_name}")
        data = r.json()
        quote_rate = data['conversion_rates'][quote_name]
        total_amount = quote_rate * amount

        return total_amount