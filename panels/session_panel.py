from panels.preset_headapi import *


@application.post(
    "/session/create",
    tags=["Session panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][0]['session-create_summary'],
    description=config['tags_metadata'][0]['session-create_description'])
async def create_session(
        input: LoginData,
        response: Response):
    passage = await SessionRepo.get_session(
        input.keyword,
        input.password)
    if passage != 'ag':
        return f'could not created session for {input.keyword}'
    else:
        session = uuid4()
        data = SessionData(username=input.keyword)
        await backend.create(
            session,
            data)
        cookie.attach_to_response(
            response,
            session)
        return f'session created for {input.keyword}'


@application.get(
    "/session/whoami",
    tags=["Session panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][0]['session-whoami_summary'],
    description=config['tags_metadata'][0]['session-whoami_description'],
    dependencies=[Depends(cookie)])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@application.get(
    "/session/delete",
    tags=["Session panel"],
    response_class=ORJSONResponse,
    summary=config['tags_metadata'][0]['session-delete_summary'],
    description=config['tags_metadata'][0]['session-delete_description'],
    dependencies=[Depends(cookie)])
async def del_session(
        response: Response,
        session_id: UUID = Depends(cookie),
        session_data: SessionData = Depends(verifier)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
    return "deleted session"



