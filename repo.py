import abc
from dataclasses import dataclass
from datetime import datetime
import hashlib

import psycopg2
from config_reader import config

connection = psycopg2.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database']
)
connection.autocommit = True


# creating 'end-point' for line with greater time interval
async def line_endpoint(dataset):
    duplicate = dataset[-1]
    duplicate[0] = datetime.timestamp(datetime.now())
    split_time = str(duplicate[0]).split(sep='.')
    stamp = split_time[0] + '000'
    duplicate[0] = int(stamp)
    dataset = list(dataset)
    dataset.append(duplicate)
    return dataset


# tuple to list
def data_converter(dataset):
    for i in range(dataset.__len__()):
        dataset[i] = list(dataset[i])
        dataset[i][0] = int(dataset[i][0])
        dataset[i][1] = float(dataset[i][1])
    return dataset


@dataclass
class PriceRecord:
    exchange: str
    symbol: str
    base: str
    quote: str
    last_price: float


class BasePriceRepo(abc.ABC):
    @abc.abstractmethod
    async def insert(
            self,
            price: int | list):
        pass


class BinancePriceRepo(BasePriceRepo):
    @staticmethod
    async def json_output(
            base,
            quote):
        with connection.cursor() as cursor:
            sql_query = f"""
                SELECT timestamp, binance_{base}_{quote}
                FROM binance_exchange_rates
                    ORDER BY timestamp;
                """
            cursor.execute(sql_query)
            db_binance_data = cursor.fetchall()
        binance_dataset = data_converter(db_binance_data)
        return binance_dataset

    async def insert(
            self,
            binance_data: list):
        dt = datetime.strptime(
            str(datetime.now()),
            "%Y-%m-%d %H:%M:%S.%f")
        splitter = str(datetime.timestamp(dt)).split(sep='.')
        timestamp = int(splitter[0] + '000')
        with connection.cursor() as cursor:
            sql_query = f"""
                        INSERT INTO binance_exchange_rates
                            (datetime, timestamp, binance_btc_usdt, binance_btc_rub, binance_usdt_rub)
                        VALUES ('{dt}', {timestamp}, {binance_data[0]}, {binance_data[1]}, {binance_data[2]});
                        """
            cursor.execute(sql_query)


class CentralBankRepo(BasePriceRepo):
    @staticmethod
    def last_value_cb():
        with connection.cursor() as cursor:
            sql_query = """
                        SELECT cbrf_usdt_rub
                        FROM cbrf_exchange_rates
                            ORDER BY timestamp DESC
                                LIMIT 1;
                        """
            cursor.execute(sql_query)
            db_cb_data = cursor.fetchall()
        cb_last_value = float(list(db_cb_data[0])[0])
        return cb_last_value

    @staticmethod
    async def json_output():
        with connection.cursor() as cursor:
            sql_query = """
                        SELECT timestamp, cbrf_usdt_rub
                        FROM cbrf_exchange_rates
                            ORDER BY timestamp;
                        """
            cursor.execute(sql_query)
            db_cb_data = cursor.fetchall()
        cb_dataset = data_converter(db_cb_data)
        cb_dataset = await line_endpoint(cb_dataset)
        return cb_dataset

    async def insert(
            self,
            cb_data: PriceRecord):
        dt = datetime.strptime(
            str(datetime.now()),
            "%Y-%m-%d %H:%M:%S.%f")
        splitter = str(datetime.timestamp(dt)).split(sep='.')
        timestamp = int(splitter[0] + '000')
        with connection.cursor() as cursor:
            sql_query = f"""
                        INSERT INTO cbrf_exchange_rates
                            (datetime, timestamp, cbrf_usdt_rub)
                        VALUES ('{dt}', {timestamp}, {cb_data})
                        """
            cursor.execute(sql_query)


class ActionRepo:
    @staticmethod
    def action_create(data):
        dt = datetime.strptime(
            str(data.dt),
            "%Y-%m-%d %H:%M:%S")
        splitter = str(datetime.timestamp(dt)).split(sep='.')
        timestamp = int(splitter[0]+'000')
        with connection.cursor() as cursor:
            sql_query = f"""
                        INSERT INTO actions 
                            (datetime, timestamp, base, quote, bought_at, quantity)
                        VALUES ('{dt}', '{timestamp}', {data.base}, {data.quote}, '{data.bought_at}', {data.quantity});
                        """
            cursor.execute(sql_query)

    @staticmethod
    def action_read():
        with connection.cursor() as cursor:
            sql_query = """
                        SELECT *
                        FROM actions;
                        """
            cursor.execute(sql_query)
            db_actions = cursor.fetchall()
        return db_actions

    @staticmethod
    def action_update(data):
        with connection.cursor() as cursor:
            sql_query = f"""
                        UPDATE actions
                        SET {data['source']} = '{data['new']}'
                            WHERE id = '{data['identity']}';
                        """
            cursor.execute(sql_query)

    @staticmethod
    def action_delete(identity):
        with connection.cursor() as cursor:
            identity = str(identity).split(sep='=')
            sql_query = f"""
                        DELETE 
                        FROM actions
                            WHERE id = {identity[1]};
                        """
            cursor.execute(sql_query)

    @staticmethod
    def action_output(
            base,
            quote):
        with connection.cursor() as cursor:
            sql_query = f"""
                        SELECT timestamp, bought_at
                        FROM actions
                            WHERE (base = '{base}' AND quote = '{quote}') 
                               ORDER BY timestamp;
                        """
            cursor.execute(sql_query)
            db_exchange_dataset = cursor.fetchall()
        exchange_dataset = data_converter(db_exchange_dataset)
        return exchange_dataset


class PushyTokenRepo:
    @staticmethod
    def device_token_output():
        with connection.cursor() as cursor:
            sql_query = """
                        SELECT device_token
                        FROM pushy_users
                            ORDER BY ID;
                        """
            cursor.execute(sql_query)
            db_data_tokens = cursor.fetchall()
        token_pool = []
        for i in range(list(db_data_tokens).__len__()):
            token_pool.append(list(db_data_tokens[i]))
        return token_pool

    @staticmethod
    async def insert(device_token):
        with connection.cursor() as cursor:
            sql_query = f"""
                        INSERT INTO pushy_users
                            (device_token)
                        VALUES {[device_token]};
                        """
            cursor.execute(sql_query)


class SessionRepo:
    @staticmethod
    def create_session(
            keyword,
            password):
        with connection.cursor() as cursor:
            sql_query = f"""
                        INSERT INTO sessions
                            (keyword, password)
                        VALUES ('{keyword}', '{hashlib.sha256(password.encode('utf-8')).hexdigest()}');
                        """
            cursor.execute(sql_query)

    @staticmethod
    async def get_session(
            keyword,
            password):
        try:
            with connection.cursor() as cursor:
                sql_query = f"""
                            SELECT keyword
                            FROM sessions 
                                WHERE password = '{hashlib.sha256(password.encode('utf-8')).hexdigest()}';
                            """
                cursor.execute(sql_query)
                db_sessions = cursor.fetchall()
            sessions = list(db_sessions[0])
            if keyword in sessions:
                return 'ag'
            else:
                return 'ad'
        except:
            return 'ad'
