from smartbox import db
from smartbox.models import Customer

def test_boxes_page_as_admin(client, app):
    """
    Testet, ob ein eingeloggter Admin auf die Boxen-Liste zugreifen kann.
    """
    # Admin erstellen und einloggen
    with app.app_context():
        admin_user = Customer(email='admin_test@example.com', first_name='Test', last_name='Admin', role='admin')
        admin_user.set_password('securepassword')
        db.session.add(admin_user)
        db.session.commit()

    client.post('/login', data={'email': 'admin_test@example.com', 'password': 'securepassword'})

    # Geschützte Seite aufrufen
    response = client.get('/boxes/')
    
    assert response.status_code == 200
    assert b"Boxen\xc3\xbcbersicht" in response.data # xc3\xbc ist das 'ü' in UTF-8

def test_boxes_page_unauthorized(client):
    """
    Prüft, ob nicht-authentifizierte Nutzer zur Login-Seite weitergeleitet werden.
    """
    response = client.get('/boxes/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Bitte melden Sie sich an" in response.data