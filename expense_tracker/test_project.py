import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_add_expense(client):
    response = client.post('/expenses', json={'day': '2024-07-30', 'expenditure': 100})
    assert response.status_code == 200
    assert 'id' in response.get_json()

def test_get_expenses(client):
    response = client.get('/expenses')
    assert response.status_code == 200
    expenses = response.get_json()
    assert isinstance(expenses, list)

def test_update_expense(client):
    # Add an expense first
    response = client.post('/expenses', json={'day': '2024-07-30', 'expenditure': 100})
    expense_id = response.get_json()['id']
    
    # Update the expense
    response = client.put(f'/expenses/{expense_id}', json={'day': '2024-07-31', 'expenditure': 200})
    assert response.status_code == 200
    assert response.get_json()['status'] == 'Expense updated'

def test_delete_expense(client):
    # Add an expense first
    response = client.post('/expenses', json={'day': '2024-07-30', 'expenditure': 100})
    expense_id = response.get_json()['id']
    
    # Delete the expense
    response = client.delete(f'/expenses/{expense_id}')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'Expense deleted'
