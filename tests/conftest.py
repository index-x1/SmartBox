import pytest
from smartbox import create_app, db
from smartbox.models import Customer

@pytest.fixture(scope='module')
def test_app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })
    return app

@pytest.fixture() # Standard-Scope ist 'function', wird also für jeden Test neu ausgeführt
def app(test_app):
    """
    Stellt für jeden einzelnen Test eine saubere Datenbank bereit.
    """
    with test_app.app_context():
        db.create_all()
        yield test_app # Hier läuft der eigentliche Test
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    """Stellt einen Test-Client für die App bereit."""
    return app.test_client()

@pytest.fixture()
def new_customer():
    """Stellt ein einfaches Kunden-Objekt für Unit-Tests bereit."""
    customer = Customer(
        first_name='Test',
        last_name='User',
        email='test@example.com',
        role='customer'
    )
    customer.set_password('password123')
    return customer