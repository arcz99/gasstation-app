import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def test_login_and_protected_page(client):
    #logowanie
    rv = login(client, "manager", "SuperSecretPassword123")
    assert b"Logout" in rv.data or b"Sales" in rv.data


    resp = client.get('/employees')
    assert resp.status_code == 200
    assert b"Employees" in resp.data