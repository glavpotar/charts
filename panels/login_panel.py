from panels.preset_headapi import *


@application.get(
    '/login',
    response_class=HTMLResponse,
    deprecated=True,
    include_in_schema=False)
async def login():
    return get_swagger_ui_html(
        openapi_url='/closeapi.json',
        title='login',
        swagger_ui_parameters={"tryItOutEnabled": True})


@application.get(
    '/closeapi.json',
    response_class=ORJSONResponse,
    deprecated=True,
    include_in_schema=False)
async def closeapi_json(request: Request):
    return templates.TemplateResponse(
        'closeapi.json',
        {'request': request})
