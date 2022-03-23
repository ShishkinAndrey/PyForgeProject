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


@pytest.mark.parametrize('request_data', [
    {
        "email": "test_email_customer",
        "password": "test_password",
        "first_name": "name",
        "last_name": "surname"
    },
    {
        "email": "test_email_doctor",
        "password": "test_password",
        "first_name": "name",
        "last_name": "surname"
    },
    {
        "email": "test_email_assistant",
        "password": "test_password",
        "first_name": "name",
        "last_name": "surname"
    },
])
def test_signup_user_already_exists(client, customer, doctor, assistant, request_data):
    response = client.post(
        '/signup',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.data == b"User already exists"


@pytest.mark.parametrize('request_data', [
    {
        "email": "test_email_customer",
        "password": "test_password",
    },
    {
        "email": "test_email_doctor",
        "password": "test_password",
    },
    {
        "email": "test_email_assistant",
        "password": "test_password",
    },
])
def test_login(client, customer, doctor, assistant, request_data):
    response = client.post(
        '/login',
        data=json.dumps(request_data),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data == b"Successfully logged in"


@pytest.mark.parametrize("email, password", [('wrong_email', 'test_password'), ('test_email_customer', 'test_password2')])
def test_login_error(client, customer, email, password):
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


@force_login('customer')
def test_logout(client, customer):
    response = client.get(
        '/logout',
    )

    assert response.status_code == 200
    assert response.data == b"Successfully logged out"
