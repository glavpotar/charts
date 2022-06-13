from panels.preset_headapi import *


@application.get(
    '/chart',
    response_class=HTMLResponse,
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False
    )
async def read_index(
        request: Request,
        session_data: SessionData = Depends(verifier)):
    return templates.TemplateResponse(
        "index.html",
        {"request": request})
