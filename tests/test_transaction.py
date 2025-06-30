import pytest
from app import app, db
from models import User, Employee, Pump, FuelType, Product

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            # Tworzenie użytkownika testowego (manager)
            if not User.query.filter_by(username="testuser").first():
                user = User(username="testuser", role="manager")
                user.set_password("testpass")
                db.session.add(user)
                db.session.commit()
                employee = Employee(first_name="Test", last_name="User", position="Manager", user_id=user.id)
                db.session.add(employee)
                db.session.commit()
            # Tworzenie produktu
            if not Product.query.filter_by(name="Pb95 Test").first():
                product = Product(name="Pb95 Test", price=7.00, product_type="fuel", stock=100, category_id=1)
                db.session.add(product)
                db.session.commit()
            # Tworzenie FuelType
            if not FuelType.query.filter_by(name="Pb95 Test").first():
                fuel_type = FuelType(name="Pb95 Test", product_id=Product.query.filter_by(name="Pb95 Test").first().id)
                db.session.add(fuel_type)
                db.session.commit()
            # Tworzenie Pompy
            if not Pump.query.filter_by(pump_number=101).first():
                pump = Pump(pump_number=101, fuel_type_id=FuelType.query.filter_by(name="Pb95 Test").first().id)
                db.session.add(pump)
                db.session.commit()
        yield client

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def test_add_transaction(client):
    # Logowanie testowym managerem
    rv = login(client, "testuser", "testpass")
    assert b"Logout" in rv.data or b"Sales" in rv.data

    # Pobranie testowej pompy
    with app.app_context():
        pump = Pump.query.filter_by(pump_number=101).first()
        assert pump is not None

    # Dodanie transakcji (tankowanie 10 litrów po 7 PLN = 70 PLN)
    data = {
        "pump_id": str(pump.id),
        "litres": "10",
        "amount": "70"
        # brak customer_id = paragon
    }
    resp = client.post("/transactions/add", data=data, follow_redirects=True)
    assert resp.status_code == 200 or resp.status_code == 302


    with app.app_context():
        product = Product.query.filter_by(name="Pb95 Test").first()
        assert product.stock == 90  # Było 100, zatankowaliśmy 10