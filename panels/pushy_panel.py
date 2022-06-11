from panels.preset_headapi import *


@application.get(
    '/repo/{api_key}',
    tags=["Insert panel"],
    response_class=HTMLResponse,
    summary=config['tags_metadata'][2]['token-insert_summary'],
    description=config['tags_metadata'][2]['token-insert_description'],
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False)
async def token_repo(
        api_key,
        session_data: SessionData = Depends(verifier)):
    await PushyTokenRepo.insert(api_key)


@application.get(
    '/service-worker.js',
    response_class=HTMLResponse,
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False)
async def read_js(
        request: Request,
        session_data: SessionData = Depends(verifier)):
    return templates.TemplateResponse(
        "service-worker.js",
        {"request": request})
