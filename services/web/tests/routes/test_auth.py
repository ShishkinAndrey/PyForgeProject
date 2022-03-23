import json

import pytest
from werkzeug.security import check_password_hash

from main import db
from models import User
from tests.conftest import force_login


def test_signup(client):
    response = client.post(
        '/signup',
        data=json.dumps(
            {
                "email": "test_email",
                "password": "test_password",
                "first_name": "name",
                "last_name": "surname"
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.data == b"Successfully sign up"

    user = db.session.query(User).first()
    assert user.email == "test_email"
    assert check_password_hash(user.password, "test_password")
    assert user.first_name == "name"
    assert user.last_name == "surname"


def test_signup_user_already_exists(client, user):
    response = client.post(
        '/signup',
        data=json.dumps(
            {
                "email": "test_email",
                "password": "test_password",
                "first_name": "name",
                "last_name": "surname"
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.data == b"User already exists"


def test_login(client, user):
    response = client.post(
        '/login',
        data=json.dumps({
                "email": "test_email",
                "password": "test_password",
            }
        ),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data == b"Successfully logged in"


@pytest.mark.parametrize("email, password", [('test_email2', 'test_password'), ('test_email', 'test_password2')])
def test_login(client, user, email, password):
    response = client.post(
        '/login',
        data=json.dumps({
                "email": email,
                "password": password,
            }
        ),
        content_type='application/json'
    )

    assert response.status_code == 400
    assert response.data == b"Incorrect email or password"


@force_login()
def test_logout(client, user):
    response = client.get(
        '/logout',
    )

    assert response.status_code == 200
    assert response.data == b"Successfully logged out"
