import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


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
