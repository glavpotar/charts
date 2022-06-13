import abc
import asyncio
import datetime
import logging
import requests
import os
from asyncio import sleep
from enum import Enum

from bs4 import BeautifulSoup
from binance import AsyncClient

from repo import PriceRecord, BasePriceRepo
from config_reader import config


BINANCE_SECS_AWAIT = 5
CB_SECS_AWAIT = 3600

logger = logging.getLogger(__name__)
fileHandler = logging.StreamHandler()
os.makedirs('logs', exist_ok=True)
consoleHandler = logging.FileHandler(f'logs/{__name__ }.log')
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
fileHandler.setFormatter(formatter)
consoleHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
logger.setLevel(logging.INFO)


class ChannelStatus(Enum):
    CREATED = 1
    SUBSCRIBING = 2
    SUBSCRIBED = 3
    WORKING = 4
    ERROR = 16


class BaseExtractor(abc.ABC):
    def __init__(self, repo: BasePriceRepo):
        self.repo = repo
        logger.info(f'initialized {self.__class__.__name__} with repo {self.repo.__class__.__name__}')

    @abc.abstractmethod
    async def run(self):
        pass


class BinanceExtractor(BaseExtractor):
    @staticmethod
    def get_symbol_mapping(exchange_info: dict) -> dict:
        result = {}
        for symbol in exchange_info['symbols']:
            s = symbol['symbol']
            base = symbol['baseAsset']
            quote = symbol['quoteAsset']
            result[s] = (base, quote)
        return result

    async def run(self):
        client = await AsyncClient.create()
        exchange_info = await client.get_exchange_info()
        symbols_mapping = self.get_symbol_mapping(exchange_info)
        logger.info(f'got exchange info from Binance: {len(symbols_mapping)} symbols exist')
        drop = 0
        while True:
            try:
                tickers = await client.get_all_tickers()
                logger.debug(f'Binance {tickers=}')
                for symbol in tickers:
                    base, quote = symbols_mapping[symbol['symbol']]
                    # USDT-RUB
                    if base == 'USDT' and quote == 'RUB':
                        binance_usdt_to_rub = PriceRecord(exchange='Binance',
                                                          symbol=symbol['symbol'],
                                                          base=base,
                                                          quote=quote,
                                                          last_price=symbol['price'],
                                                          )
                        drop += 1
                    #BTC-USDT
                    elif base == 'BTC' and quote == 'USDT':
                        binance_btc_to_usdt = PriceRecord(exchange='Binance',
                                                          symbol=symbol['symbol'],
                                                          base=base,
                                                          quote=quote,
                                                          last_price=symbol['price'],
                                                          )
                        drop += 1
                    #BTC-RUB
                    elif base == 'BTC' and quote == 'RUB':
                        binance_btc_to_rub = PriceRecord(exchange='Binance',
                                                         symbol=symbol['symbol'],
                                                         base=base,
                                                         quote=quote,
                                                         last_price=symbol['price'],
                                                         )
                        drop += 1
                    #collected
                    if drop == 3:
                        await self.repo.insert([binance_btc_to_usdt.last_price, binance_btc_to_rub.last_price, binance_usdt_to_rub.last_price])
                        drop = 0
                        await sleep(config['BINANCE_SECS_AWAIT'])
            except Exception as e:
                try:
                    await AsyncClient.close_connection(client)
                    client = await AsyncClient.create()
                    exchange_info = await client.get_exchange_info()
                    symbols_mapping = self.get_symbol_mapping(exchange_info)
                    drop = 0
                    logger.exception(f'reloading because of {e}')
                except:
                    await asyncio.sleep(5)
                finally:
                    continue


class CentralBankExtractor(BaseExtractor):
    async def run(self):
        while True:
            for i in range(1):
                response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp').text
                soup = BeautifulSoup(response)
                price = soup.findAll("valute", {"id": "R01235"})[0].select('value')[0].getText()
                price = float(price.replace(',', '.'))
                cb_data = PriceRecord(exchange='CentralBank',
                                      symbol='',
                                      base='',
                                      quote='',
                                      last_price=price
                                      )
                await self.repo.insert(cb_data.last_price)
            await asyncio.sleep(config['CB_SECS_AWAIT'])


