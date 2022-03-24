import io
import json

from models import MedicalTestOrder
from tests.conftest import force_login


@force_login('doctor')
def test_get_orders_by_doctor(client, medical_test_order):
    response = client.get(
        'orders/',
    )

    assert response.status_code == 200
    assert response.json == {'data': [
        {
            'id': 1,
            'test': 1,
            'customer': 1,
            'access': 2,
            'status': 'created',
            'result': None
        },
    ]}


@force_login('customer')
def test_get_orders_by_customer(client, customer):
    response = client.get(
        'orders/',
    )

    assert response.status_code == 403


@force_login('assistant')
def test_get_orders_by_assistant(client, assistant):
    response = client.get(
        'orders/',
    )

    assert response.status_code == 403


@force_login('doctor')
def test_get_order_by_id_by_doctor(client, medical_test_order):
    response = client.get(
        'orders/1',
    )

    assert response.status_code == 200
    assert response.json == {
            'id': 1,
            'test': 1,
            'customer': 1,
            'access': 2,
            'status': 'created',
            'result': None
    }


@force_login('doctor')
def test_get_order_by_wrong_id_by_doctor(client, medical_test_order):
    response = client.get(
        'orders/100',
    )

    assert response.status_code == 404


@force_login('customer')
def test_get_order_by_id_by_customer(client, medical_test_order, customer):
    response = client.get(
        'orders/1',
    )

    assert response.status_code == 403


@force_login('assistant')
def test_get_order_by_id_by_assistant(client, medical_test_order, assistant):
    response = client.get(
        'orders/1',
    )

    assert response.status_code == 403


@force_login('customer')
def test_make_an_order(client, customer, doctor, medical_test_order):
    response = client.post(
        'orders/',
        data=json.dumps(
            {
                'test': 1,
                'access': 2,
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.data == b'Order is created'


@force_login('customer')
def test_make_an_order_access_not_found(client, customer, doctor, medical_test_order):
    response = client.post(
        'orders/',
        data=json.dumps(
            {
                'test': 1,
                'access': 3,
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 404


@force_login('customer')
def test_add_access(client, customer, doctor, medical_test_order_without_access):
    response = client.patch(
        'orders/1/access',
        data=json.dumps(
            {
                'access': 2,
            }
        ),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.data == b'Access for test is added'


@force_login('assistant')
def test_add_result(client, assistant, medical_test_order):
    data = {}
    data['file'] = (io.BytesIO(b'test_file'), 'test.pdf')
    response = client.post(
        'orders/1/result',
        data=data,
        content_type='multipart/form-data'
        )
    assert response.status_code == 200
    assert response.data == b'Result is added'
    order = MedicalTestOrder.query.filter(MedicalTestOrder.id == 1).first()

    assert order.result == 'test.pdf'
    assert order.status == 'ready'
