from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from repo import CentralBankRepo, BinancePriceRepo


application = FastAPI()
directory = "templates"
templates = Jinja2Templates(directory=directory)


@application.get('/', response_class=HTMLResponse)
def read_index(request: Request):
    CentralBankRepo.json_output_cb()
    BinancePriceRepo.json_output_binance()
    return templates.TemplateResponse("index.html", {"request": request})


class ChartStarter:
    @staticmethod
    def starter():
        uvicorn.run(application, host='127.0.0.1', port='8220')


ChartStarter.starter()
