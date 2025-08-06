from smartbox import db
from smartbox.models import Customer

def test_admin_login_and_logout(client, app):
    """
    Testet den Login- und Logout-Vorgang für einen Admin.
    """
    # Schritt 1: Admin-Benutzer in der leeren Test-DB erstellen
    with app.app_context():
        admin_user = Customer(email='admin_test@example.com', first_name='Test', last_name='Admin', role='admin')
        admin_user.set_password('securepassword')
        db.session.add(admin_user)
        db.session.commit()

    # Schritt 2: Simuliere den Login
    response_login = client.post('/login', data={
        'email': 'admin_test@example.com',
        'password': 'securepassword'
    }, follow_redirects=True)
    
    assert response_login.status_code == 200
    assert b'Willkommen im SmartBox System' in response_login.data # Prüft, ob wir auf der Hauptseite sind

    # Schritt 3: Simuliere den Logout
    response_logout = client.get('/logout', follow_redirects=True)
    assert response_logout.status_code == 200
    assert b'Willkommen im SmartBox System' in response_logout.data


def test_customer_page_access_as_admin(client, app):
    """
    Testet, ob ein eingeloggter Admin auf die Kundenliste zugreifen kann.
    """
    # Schritt 1: Admin erstellen (DB ist für diesen Test wieder sauber)
    with app.app_context():
        admin_user = Customer(email='admin_test@example.com', first_name='Test', last_name='Admin', role='admin')
        admin_user.set_password('securepassword')
        db.session.add(admin_user)
        db.session.commit()

    # Schritt 2: Einloggen
    client.post('/login', data={'email': 'admin_test@example.com', 'password': 'securepassword'})

    # Schritt 3: Geschützte Seite aufrufen
    response_customers = client.get('/customers/')
    
    # Prüfen, ob der Zugriff erfolgreich ist (Status 200) und die Seite geladen wird
    assert response_customers.status_code == 200
    assert b"Kunden\xc3\xbcbersicht" in response_customers.data # xc3\xbc ist das 'ü' in UTF-8