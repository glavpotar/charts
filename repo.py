import abc
import json
from dataclasses import dataclass, field
from datetime import datetime

import psycopg2

from host import *


connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
connection.autocommit = True


# creating 'end-point' for line with greater time interval
def line_endpoint(dataset):
    duplicate = dataset[-1]
    duplicate[0] = datetime.timestamp(datetime.now())
    split_time = str(duplicate[0]).split(sep='.')
    stamp = split_time[0] + '000'
    duplicate[0] = int(stamp)
    dataset = list(dataset)
    dataset.append(duplicate)
    return dataset


#tuple to list
def data_converter(dataset):
    for i in range(dataset.__len__()):
        dataset[i] = list(dataset[i])
        time_str = datetime.strptime(dataset[i][0], "%Y-%m-%d %H:%M:%S.%f")
        splitter = str(datetime.timestamp(time_str)).split(sep='.')
        splitter = splitter[0]+'000'
        dataset[i][0] = int(splitter)
        dataset[i][1] = float(dataset[i][1])
    return dataset


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
    @staticmethod
    def json_output_binance():
        with connection.cursor() as cursor:
            cursor.execute("""SELECT time_received, price
                                  FROM binance_data
                                  ORDER BY ID""")
            db_binance_data = cursor.fetchall()
        binance_dataset = data_converter(db_binance_data)
        with open('jsons/binance.json', 'w') as out_file:
            json.dump(binance_dataset, out_file)

    async def insert(self, binance_data: PriceRecord):
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO binance_data (val, time_received, price)
                           VALUES (%s, %s, %s);""",
                           (binance_data.quote, binance_data.time_received, binance_data.last_price))


class CentralBankRepo(BasePriceRepo):
    @staticmethod
    def json_output_cb():
        with connection.cursor() as cursor:
            cursor.execute("""SELECT time_received, price
                                   FROM central_bank_data
                                   ORDER BY ID""")
            db_cb_data = cursor.fetchall()
        cb_dataset = data_converter(db_cb_data)
        cb_dataset = line_endpoint(cb_dataset)
        with open('jsons/cb.json', 'w') as out_file:
            json.dump(cb_dataset, out_file)

    async def insert(self, cb_data: PriceRecord):
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO central_bank_data (time_received, price)
                           VALUES (%s, %s)""",
                           (cb_data.time_received, cb_data.last_price))
