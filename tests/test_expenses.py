import random
import json
import datetime
import pytest
from src.services import ExpensesApiService

expense_api = ExpensesApiService()


@pytest.fixture(scope='module')
def create_expense_id(sign_up_response, headers, car_id):
    current_timestamp = datetime.datetime.now().isoformat()
    mileage = random.randint(2, 13)
    payload = {
        "carId": car_id,
        "reportedAt": current_timestamp,
        "mileage": mileage,
        "liters": 11,
        "totalCost": 11,
        "forceMileage": False
    }
    response = expense_api.create_an_expense(body=json.dumps(payload), headers=headers)
    expense_id = response.get_field('data')['id']
    return expense_id


def test_create_an_expense(sign_up_response, headers, car_id):
    current_timestamp = datetime.datetime.now().isoformat()
    mileage = random.randint(14, 210)
    liters = random.randint(15, 75)
    total = liters * 3
    payload = {
        "carId": car_id,
        "reportedAt": current_timestamp,
        "mileage": mileage,
        "liters": liters,
        "totalCost": total,
        "forceMileage": False
    }
    response = expense_api.create_an_expense(body=json.dumps(payload), headers=headers)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['reportedAt'] == payload['reportedAt']
    assert response.get_field('data')['mileage'] == payload['mileage']
    assert response.get_field('data')['liters'] == payload['liters']
    assert response.get_field('data')['totalCost'] == payload['totalCost']
    assert response.get_field('data')['carId'] == payload['carId']


def test_expenses_list(sign_up_response, headers):
    response = expense_api.get_all_expenses(headers)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'


def test_get_expense_by_id(sign_up_response, headers, create_expense_id):
    response = expense_api.get_an_expense_by_id(headers=headers, expense_ids=create_expense_id)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'


def test_edit_expense(sign_up_response, headers, car_id, create_expense_id):
    current_timestamp = datetime.datetime.now().isoformat()
    mileage = random.randint(211, 2100)
    liters = random.randint(15, 75)
    total = liters * 3
    payload = {
        "carId": car_id,
        "reportedAt": current_timestamp,
        "mileage": mileage,
        "liters": liters,
        "totalCost": total,
        "forceMileage": False
    }
    response = expense_api.edit_an_expense(body=json.dumps(payload), headers=headers, expense_ids=create_expense_id)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['reportedAt'] == payload['reportedAt']
    assert response.get_field('data')['mileage'] == payload['mileage']
    assert response.get_field('data')['liters'] == payload['liters']
    assert response.get_field('data')['totalCost'] == payload['totalCost']
    assert response.get_field('data')['carId'] == payload['carId']


def test_remove_expense(sign_up_response, headers, create_expense_id):
    response = expense_api.removes_an_expense(headers=headers, expense_ids=create_expense_id)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert int(response.get_field('data')['expenseId']) == int(create_expense_id)
