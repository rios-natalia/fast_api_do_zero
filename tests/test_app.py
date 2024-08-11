from http import HTTPStatus

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import select

from fast_zero.app import app, check_user_exists
from fast_zero.models import User


def test_create_user(client, default_user):
    client = TestClient(app)

    response = client.post('/users/', json=default_user)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_get_user(client, default_user, default_user_public):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == default_user_public


def test_read_users(client, default_user_public):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [default_user_public]}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_put_user_not_found(client, user_not_found):
    response = client.put('/users/100', json=user_not_found)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_not_found(client):
    response = client.delete('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_check_user_exists_error_not_found():
    with pytest.raises(HTTPException) as exception:
        check_user_exists(1000)

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.detail == 'User not found'


def test_create_db_user(session):
    new_user = User(
        username='alice', password='secret', email='alice@example.com'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
