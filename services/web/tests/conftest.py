import functools

from flask.testing import FlaskClient
import pytest
from werkzeug.security import generate_password_hash

from config import TestingConfig
from main import create_app, db
from models import Role, User


@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object(TestingConfig)
    with app.app_context():
        db.create_all()
        db.session.add(Role(
            name="customer",
        ))
        db.session.add(Role(
            name="doctor",
        ))
        db.session.add(Role(
            name="assistant",
        ))
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture
def user():
    db.session.add(User(
        email="test_email",
        password=generate_password_hash("test_password", method='sha256'),
        first_name="name",
        last_name="surname"
    ))
    db.session.commit()


def force_login():
    def inner(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for key, val in kwargs.items():
                if isinstance(val, FlaskClient):
                    with val:
                        with val.session_transaction() as sess:
                            user = User.query.first()
                            sess['_user_id'] = user.id
                        return f(*args, **kwargs)
            return f(*args, **kwargs)

        return wrapper

    return inner