from panels.preset_headapi import *


@application.get(
    '/swagger',
    response_class=HTMLResponse,
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False)
async def swagger(session_data: SessionData = Depends(verifier)):
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='swagger',
        swagger_ui_parameters={"tryItOutEnabled": True})


@application.get(
    '/openapi.json',
    response_class=ORJSONResponse,
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False)
async def openapi_json(session_data: SessionData = Depends(verifier)):
    return application.openapi()


@application.get(
    '/',
    response_class=HTMLResponse,
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False)
async def redir(session_data: SessionData = Depends(verifier)):
    response = RedirectResponse(url='/swagger')
    return response


@application.get(
    '/docs',
    response_class=HTMLResponse,
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False)
async def redir(session_data: SessionData = Depends(verifier)):
    response = RedirectResponse(url='/swagger')
    return response
