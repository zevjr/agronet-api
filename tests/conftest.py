from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app import create_app


class Session:
    ...
    # esse Session, deve ser removida
    # e substituida pelo Session do seu ORM


@pytest.fixture
def app():
    return create_app()


@pytest.fixture(scope="function")
def create_token() -> str:
    return "token"


@pytest.fixture(scope="function")
def header(create_token) -> dict:
    return {"token": create_token}


@pytest.fixture(scope="function")
def url_v1() -> str:
    return "/api/v1"


@pytest.fixture(name="session")
def session():
    ...
    # deve implementar a sessao com base no ORM escolhido.


@pytest.fixture(scope="function")
def client(app, session: Session) -> Generator:
    def get_session_override():
        return session

    app.dependency_overrides["get_session"] = get_session_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
