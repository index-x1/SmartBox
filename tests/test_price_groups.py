from smartbox import db
from smartbox.models import Customer

def test_price_groups_page_as_admin(client, app):
    """
    Testet, ob ein eingeloggter Admin auf die Preisgruppen-Liste zugreifen kann.
    """
    # Admin erstellen und einloggen
    with app.app_context():
        admin_user = Customer(email='admin_test@example.com', first_name='Test', last_name='Admin', role='admin')
        admin_user.set_password('securepassword')
        db.session.add(admin_user)
        db.session.commit()

    client.post('/login', data={'email': 'admin_test@example.com', 'password': 'securepassword'})

    # Geschützte Seite aufrufen
    response = client.get('/price-groups/')
    
    assert response.status_code == 200
    assert b"Preisgruppen" in response.data

def test_price_groups_page_unauthorized(client):
    """
    Prüft, ob nicht-authentifizierte Nutzer zur Login-Seite weitergeleitet werden.
    """
    response = client.get('/price-groups/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Bitte melden Sie sich an" in response.data