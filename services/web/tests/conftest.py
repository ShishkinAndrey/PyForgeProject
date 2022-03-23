import functools

from flask.testing import FlaskClient
import pytest
from werkzeug.security import generate_password_hash

from config import TestingConfig
from main import create_app, db
from models import Role, User, Category, MedicalTest


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


@pytest.fixture
def customer():
    db.session.add(User(
        email="test_email_customer",
        password=generate_password_hash("test_password", method='sha256'),
        first_name="name",
        last_name="surname",
        role=1
    ))
    db.session.commit()


@pytest.fixture
def doctor():
    db.session.add(User(
        email="test_email_doctor",
        password=generate_password_hash("test_password", method='sha256'),
        first_name="name",
        last_name="surname",
        role=2
    ))
    db.session.commit()


@pytest.fixture
def assistant():
    db.session.add(User(
        email="test_email_assistant",
        password=generate_password_hash("test_password", method='sha256'),
        first_name="name",
        last_name="surname",
        role=3
    ))
    db.session.commit()


@pytest.fixture
def client(app):
    yield app.test_client()


def force_login(role=None):
    def inner(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for key, val in kwargs.items():
                if isinstance(val, FlaskClient):
                    with val:
                        with val.session_transaction() as sess:
                            role_id = db.session.query(Role).filter(Role.name == role).first().id
                            user = User.query.filter(User.role == role_id).first()
                            sess['_user_id'] = user.id
                        return f(*args, **kwargs)
            return f(*args, **kwargs)

        return wrapper

    return inner


@pytest.fixture
def medical_tests():
    db.session.add(Category(
        name="a",
    ))
    db.session.add(Category(
        name="b",
    ))
    db.session.add(Category(
        name="c",
    ))
    db.session.commit()

    db.session.add(MedicalTest(
        name="a",
        category_id=1
    ))
    db.session.add(MedicalTest(
        name="b",
        category_id=1
    ))
    db.session.add(MedicalTest(
        name="c",
        category_id=3
    ))
    db.session.add(MedicalTest(
        name="f",
        category_id=2
    ))
    db.session.add(MedicalTest(
        name="r",
        category_id=3
    ))
    db.session.commit()
