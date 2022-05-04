import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from repo import JSONRegulator


application = FastAPI()
directory = ""
templates = Jinja2Templates(directory=directory)


@application.get('/', response_class=HTMLResponse)
async def read_index():
    pass
#check codepen


@application.get('/cb', response_class=ORJSONResponse)
async def cb_chart_data():
    cb_data = JSONRegulator.json_output_cb()
    return cb_data


@application.get('/binance', response_class=ORJSONResponse)
async def binance_chart_data():
    binance_data = JSONRegulator.json_output_binance()
    return binance_data
