from panels.preset_headapi import *


@application.get(
    '/cb',
    tags=["JSON panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][3]['cb_summary'],
    description=config['tags_metadata'][3]['cb_description'],
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False)
async def cb(session_data: SessionData = Depends(verifier)):
    output = await CentralBankRepo.json_output()
    return output


@application.get(
    '/json/{base}_{quote}',
    tags=["JSON panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][3]['btc-rub_summary'],
    description=config['tags_metadata'][3]['btc-rub_description'],
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False)
async def btc_rub(
        base: str,
        quote: str,
        session_data: SessionData = Depends(verifier)):
    output = await BinancePriceRepo.json_output(
        base,
        quote)
    return output
