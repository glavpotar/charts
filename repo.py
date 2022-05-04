import abc
from dataclasses import dataclass, field
from datetime import datetime

import psycopg2

from host import *


connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    db_name=db_name
)
#another db
connection.autocommit = True


def list_er(tuple):
    for i in range(tuple.__len__()):
        tuple[i] = list(tuple[i])
    return tuple


@dataclass
class PriceRecord:
    exchange: str
    symbol: str
    base: str
    quote: str
    last_price: float
    time_received: datetime = field(default_factory=datetime.now)


class BasePriceRepo(abc.ABC):
    @abc.abstractmethod
    async def insert(self, record: PriceRecord):
        pass


class BinancePriceRepo(BasePriceRepo):
    async def insert(self, binance_data: PriceRecord):
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO binance_data (val, time_received, price)
                           VALUES (%s, %s, %s);""",
                           (binance_data.quote, binance_data.time_received, binance_data.last_price))


class CentralBankRepo(BasePriceRepo):
    async def insert(self, cb_data: PriceRecord):
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO central_bank_data (time_received, price)
                           VALUES (%s, %s)""",
                           (cb_data.time_received, cb_data.last_price))


class JSONRegulator:
    @staticmethod
    async def json_output_binance():
        with connection.cursor() as cursor:
            cursor.execute("""SELECT time_received, price
                           FROM binance_data
                           ORDER BY ID""")
            db_binance_data = cursor.fetchall()
        binance_dataset = list_er(db_binance_data)
        return binance_dataset

    @staticmethod
    async def json_output_cb():
        with connection.cursor() as cursor:
            cursor.execute("""SELECT time_received, price
                           FROM centralbank_data
                           ORDER BY ID""")
            db_cb_data = cursor.fetchall()
        cb_dataset = list_er(db_cb_data)
        return cb_dataset
