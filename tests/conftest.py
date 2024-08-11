import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user_not_found():
    return {
        'username': 'notfound',
        'email': 'notfound@example.com',
        'password': 'notfound',
    }


@pytest.fixture
def default_user():
    return {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }


@pytest.fixture
def default_user_public():
    return {'username': 'alice', 'email': 'alice@example.com', 'id': 1}


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
