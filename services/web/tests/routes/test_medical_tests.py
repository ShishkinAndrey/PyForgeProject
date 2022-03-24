from tests.conftest import force_login


@force_login('customer')
def test_get_medical_tests_by_customer(client, customer, medical_tests):
    response = client.get(
        'medical_tests/',
    )

    assert response.status_code == 200
    assert response.json == {'data': [
        {
            'category': 'Blood Disorder tests',
            'category_id': 1,
            'medical_test': 'Antibodies Screen Blood Test',
            'medical_test_id': 1
        },
        {
            'category': 'Blood Disorder tests',
            'category_id': 1,
            'medical_test': 'D-Dimer Blood Test',
            'medical_test_id': 2
        },
        {
            'category': 'Blood Disorder tests',
            'category_id': 1,
            'medical_test': 'Vitamin K1 Blood Test',
            'medical_test_id': 3
        },
        {
            'category': 'Diabetes tests',
            'category_id': 2,
            'medical_test': 'Insulin Fasting Blood Test',
            'medical_test_id': 4
        },
        {
            'category': 'Diabetes tests',
            'category_id': 2,
            'medical_test': 'Glucose Serum Test',
            'medical_test_id': 5
        },
        {
            'category': 'Diabetes tests',
            'category_id': 2,
            'medical_test': 'C-Peptide Serum Test',
            'medical_test_id': 6
        },
        {
            'category': 'Immunity Tests',
            'category_id': 3,
            'medical_test': 'Immunity Blood Test Panel',
            'medical_test_id': 7
        },
        {
            'category': 'Immunity Tests',
            'category_id': 3,
            'medical_test': 'Antibodies Screen Blood Test',
            'medical_test_id': 8
        }
    ]}


@force_login('doctor')
def test_get_medical_tests_by_doctor(client, doctor, medical_tests):
    response = client.get(
        'medical_tests/',
    )

    assert response.status_code == 403


@force_login('assistant')
def test_get_medical_tests_by_assistant(client, assistant, medical_tests):
    response = client.get(
        'medical_tests/',
    )

    assert response.status_code == 403


@force_login('customer')
def test_get_medical_tests_by_id(client, customer, medical_tests):
    response = client.get(
        'medical_tests/1',
    )

    assert response.status_code == 200
    assert response.json == {'data': [
        {
            'name': 'Antibodies Screen Blood Test',
            'id': 1
        },
        {
            'name': 'D-Dimer Blood Test',
            'id': 2
        },
        {
            'name': 'Vitamin K1 Blood Test',
            'id': 3
        }]
    }


@force_login('customer')
def test_get_medical_tests_by_incorrect_id(client, customer, medical_tests):
    response = client.get(
        'medical_tests/100',
    )

    assert response.status_code == 404


@force_login('doctor')
def test_get_medical_tests_by_id_by_doctor(client, doctor, medical_tests):
    response = client.get(
        'medical_tests/1',
    )

    assert response.status_code == 403


@force_login('assistant')
def test_get_medical_tests_by_id_by_assistant(client, assistant, medical_tests):
    response = client.get(
        'medical_tests/1',
    )

    assert response.status_code == 403
