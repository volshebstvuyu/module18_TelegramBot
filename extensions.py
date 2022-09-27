import requests
import json
from constants import currency

class APIException(Exception):
    pass

class Exchange:
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Нет возможности конвертировать валюту в саму себя')

        try:
            for key, value in currency.items():
                if base in value:
                    base_item = key
        except KeyError:
            raise APIException(f'Нет такой валюты: {base}')

        try:
            for key, value in currency.items():
                if quote in value:
                    quote_item = key
        except KeyError:
            raise APIException(f'Нет такой валюты: {quote}')

        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f'Не смог обработать количество {amount}\nТы хрень понаписал, Dude')

        request = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_item}&tsyms={quote_item}')
        total_base = float(json.loads(request.content)[quote_item]) * float(amount)
        return total_base
