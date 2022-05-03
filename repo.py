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
connection.autocommit = True


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
            cursor.execute("""INSERT INTO users (val, ti_re, price)
            VALUES (%s, %s, %s);""", (binance_data.quote, binance_data.time_received, binance_data.last_price))


class CentralBankRepo(BasePriceRepo):
    async def insert(self, cb_data: PriceRecord):
        with connection.cursor() as cursor:  # TODO create 2nd db
            cursor.execute("""UPDATE users SET cb_price = %s  
            WHERE id=(SELECT max(id) FROM users);""", [cb_data.last_price])

