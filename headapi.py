from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from repo import CentralBankRepo, BinancePriceRepo


application = FastAPI()
directory = "templates"
templates = Jinja2Templates(directory=directory)


@application.get('/', response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@application.get('/cb', response_class=ORJSONResponse)
async def cb_chart_data():
    cb_data = CentralBankRepo.json_output_cb()
    return cb_data


@application.get('/binance', response_class=ORJSONResponse)
async def binance_chart_data():
    binance_data = BinancePriceRepo.json_output_binance()
    return binance_data


class ChartStarter:
    @staticmethod
    def starter():
        uvicorn.run(application, host='127.0.0.1', port='8220')


ChartStarter.starter()
