import asyncio

from extract import BinanceExtractor, CentralBankExtractor
from repo import BinancePriceRepo, CentralBankRepo, config


async def main():
    binance_repo = BinancePriceRepo()
    cb_repo = CentralBankRepo()
    extractors = [
        BinanceExtractor(binance_repo),
        CentralBankExtractor(cb_repo)]

    for extractor in extractors:
        asyncio.create_task(
            extractor.run(),
            name=extractor.__class__.__name__)

    while True:
        await asyncio.sleep(config['NOTIFICATION_SECS_AWAIT'])


if __name__ == '__main__':
    asyncio.run(main())


