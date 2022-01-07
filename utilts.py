import json
import requests
from config import exchanges


class APIExeption(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {base}')

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIExeption(f'Не удалось обработать валюту {sym}')

        if base_key == sym_key:
            raise APIExeption(f'Невозможно перевести одинаковые ввалюты {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'Не удалось обработать количество {amount}')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_key}&tsyms={sym_key}")
        resp = json.loads(r.content)
        new_price = resp[sym_key] * amount
        new_price = round(new_price, 3)
        message = f"Стоимость {amount} {base} в {sym} составляет: {new_price}."

        return message
