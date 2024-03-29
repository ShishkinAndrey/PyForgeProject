import functools

from flask.testing import FlaskClient
import pytest
from werkzeug.security import generate_password_hash

from config import TestingConfig
from main import create_app, db
from models import Category, MedicalTest, MedicalTestOrder, Role, User


@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object(TestingConfig)
    with app.app_context():
        db.create_all()
        db.session.add(Role(
            name='customer',
        ))
        db.session.add(Role(
            name='doctor',
        ))
        db.session.add(Role(
            name='assistant',
        ))
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def customer():
    db.session.add(User(
        email='test_email_customer',
        password=generate_password_hash('test_password', method='sha256'),
        first_name='name',
        last_name='surname',
        role=1
    ))
    db.session.commit()


@pytest.fixture
def doctor():
    db.session.add(User(
        email='test_email_doctor',
        password=generate_password_hash('test_password', method='sha256'),
        first_name='name',
        last_name='surname',
        role=2
    ))
    db.session.commit()


@pytest.fixture
def assistant():
    db.session.add(User(
        email='test_email_assistant',
        password=generate_password_hash('test_password', method='sha256'),
        first_name='name',
        last_name='surname',
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
        name='Blood Disorder tests',
    ))
    db.session.add(Category(
        name='Diabetes tests',
    ))
    db.session.add(Category(
        name='Immunity Tests',
    ))
    db.session.commit()

    db.session.add(MedicalTest(
        name='Antibodies Screen Blood Test',
        category_id=1
    ))
    db.session.add(MedicalTest(
        name='D-Dimer Blood Test',
        category_id=1
    ))
    db.session.add(MedicalTest(
        name='Vitamin K1 Blood Test',
        category_id=1
    ))
    db.session.add(MedicalTest(
        name='Insulin Fasting Blood Test',
        category_id=2
    ))
    db.session.add(MedicalTest(
        name='Glucose Serum Test',
        category_id=2
    ))
    db.session.add(MedicalTest(
        name='C-Peptide Serum Test',
        category_id=2
    ))
    db.session.add(MedicalTest(
        name='Immunity Blood Test Panel',
        category_id=3
    ))
    db.session.add(MedicalTest(
        name='Antibodies Screen Blood Test',
        category_id=3
    ))
    db.session.commit()


@pytest.fixture
def medical_test_order(medical_tests, customer, doctor):
    medical_test = MedicalTest.query.first()
    test_customer = User.query.filter(User.role == 1).first()
    test_access = User.query.filter(User.role == 2).first()
    db.session.add(MedicalTestOrder(
        test=medical_test.id,
        customer=test_customer.id,
        access=test_access.id,
    ))
    db.session.commit()


@pytest.fixture
def medical_test_order_without_access(medical_tests, customer):
    medical_test = MedicalTest.query.first()
    test_customer = User.query.filter(User.role == 1).first()
    db.session.add(MedicalTestOrder(
        test=medical_test.id,
        customer=test_customer.id,
    ))
    db.session.commit()
