from panels.preset_headapi import *


@application.post(
    '/action/create/',
    tags=[
        "Insert panel",
        "Action panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][1]['action-insert_summary'],
    description=config['tags_metadata'][1]['action-insert_description'],
    dependencies=[Depends(cookie)])
async def action_create(
        input: ActionCreate = Body(
            default=config['tags_metadata'][1]['action-insert_example'][0]),
        session_data: SessionData = Depends(verifier)):
    try:
        ActionRepo.action_create(input)
        return 1
    except:
        return 0


@application.get(
    '/action/read',
    tags=["Action panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][1]['action-read_summary'],
    description=config['tags_metadata'][1]['action-read_summary'],
    dependencies=[Depends(cookie)])
async def action_read(session_data: SessionData = Depends(verifier)):
    return ActionRepo.action_read()


@application.post(
    '/action/update',
    tags=["Action panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][1]['action-update_summary'],
    description=config['tags_metadata'][1]['action-update_description'],
    dependencies=[Depends(cookie)])
async def action_update(
        input: ActionUpdate = Body(
            default=config['tags_metadata'][1]['action-update_example'][0]),
        session_data: SessionData = Depends(verifier)):
    ActionRepo.action_update(input)


@application.post(
    '/action/delete',
    tags=["Action panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][1]['action-delete_summary'],
    description=config['tags_metadata'][1]['action-delete_description'],
    dependencies=[Depends(cookie)])
async def action_delete(
        input: ActionDelete = Body(
            default=config['tags_metadata'][1]['action-delete_example'][0]),
        session_data: SessionData = Depends(verifier)):
    ActionRepo.action_delete(input)


@application.get(
    '/action/output/{base}_{quote}',
    tags=[
        "Action panel",
        "JSON panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][1]['action-output_summary'],
    description=config['tags_metadata'][1]['action-output_description'],
    dependencies=[Depends(cookie)],
    deprecated=True,
    include_in_schema=False)
async def action_output(
        base: str,
        quote: str,
        session_data: SessionData = Depends(verifier)):
    output = ActionRepo.action_output(
        base,
        quote)
    return output
