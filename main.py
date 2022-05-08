import asyncio

from extract import BinanceExtractor, CentralBankExtractor
from repo import BinancePriceRepo, CentralBankRepo


async def main():
    binance_repo = BinancePriceRepo()
    cb_repo = CentralBankRepo()

    extractors = [BinanceExtractor(binance_repo), CentralBankExtractor(cb_repo)]

    for extractor in extractors:
        asyncio.create_task(extractor.run(), name=extractor.__class__.__name__)

    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
