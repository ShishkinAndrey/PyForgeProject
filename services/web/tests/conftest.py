import pytest, os

from config import TestingConfig
from main import create_app, db
from models import Role


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
    testing_client = app.test_client()

    yield testing_client  # this is where the testing happens!
