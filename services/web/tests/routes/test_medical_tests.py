from tests.conftest import force_login


@force_login()
def test_get_medical_tests(client, medical_tests):
    response = client.get(
        'medical_tests/',
    )

    assert response.status_code == 200
    assert response.json == {'data': [
        {
            "category": "a",
            "category_id": 1,
            "medical_test": "a",
            "medical_test_id": 1
        },
        {
            "category": "a",
            "category_id": 1,
            "medical_test": "b",
            "medical_test_id": 2
        },
        {
            "category": "c",
            "category_id": 3,
            "medical_test": "c",
            "medical_test_id": 3
        },
        {
            "category": "b",
            "category_id": 2,
            "medical_test": "f",
            "medical_test_id": 4
        },
        {
            "category": "c",
            "category_id": 3,
            "medical_test": "r",
            "medical_test_id": 5
        }
    ]}


@force_login()
def test_get_medical_tests_by_id(client, medical_tests):
    response = client.get(
        'medical_tests/1',
    )

    assert response.status_code == 200
    assert response.json == {'data': [
        {
            "name": "a",
            "id": 1
        },
        {
            "name": "b",
            "id": 2
        }]
    }


@force_login()
def test_get_medical_tests_by_incorrect_id(client, medical_tests):
    response = client.get(
        'medical_tests/100',
    )

    assert response.status_code == 404
