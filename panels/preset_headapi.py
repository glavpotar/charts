from uuid import uuid4


from fastapi.templating import Jinja2Templates
from fastapi.responses import ORJSONResponse, HTMLResponse
from fastapi import HTTPException, FastAPI, Response, Depends, Body, Request
from starlette.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from uuid import UUID
import uvicorn

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters

from pydantic import BaseModel

from config_reader import config

from repo import *

directory = "templates"
templates = Jinja2Templates(directory=directory)

tags_metadata = config['tags_metadata']

cookie_params = CookieParameters()

application = FastAPI(
    openapi_tags=tags_metadata,
    redoc_url=config['redoc_url'],
    docs_url=config['docs_url'],
    title=config['title'],
    description=config['description'],
    contact=config['contact'][0],
    version=config['version'],
    swagger_ui_parameters={"tryItOutEnabled": True},
    openapi_url='')


class ActionCreate(BaseModel):
    base: str
    quote: str
    bought_at: float
    quantity: float
    dt: str


class ActionUpdate(BaseModel):
    old: str
    new: str
    identity: int


class ActionDelete(BaseModel):
    identity: int


class LoginData(BaseModel):
    keyword: str
    password: str


class SessionData(BaseModel):
    username: str


cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,)

backend = InMemoryBackend[
    UUID,
    SessionData]()


class BasicVerifier(SessionVerifier[
                        UUID,
                        SessionData]):
    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: InMemoryBackend[UUID, SessionData],
            auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(
        status_code=403,
        detail="invalid session"))
