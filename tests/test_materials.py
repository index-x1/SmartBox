from smartbox.models import Material, PriceGroup
from smartbox import db

def test_new_material(app):
    """
    Test-ID: QUAL-01.3
    Prüft, ob ein Material-Objekt korrekt erstellt und gespeichert wird.
    """
    with app.app_context():
        pg = PriceGroup(name="Test-Gruppe", price_per_kg=10.0)
        
        mat = Material(
            name="Test-Material",
            description="Eine Beschreibung",
            price_group=pg # Direkte Zuweisung des Objekts ist sauberer
        )
        
        db.session.add(pg)
        db.session.add(mat)
        db.session.commit()
        
        # === KORREKTUR: Abfrage und Assertions innerhalb des Contexts ===
        retrieved_mat = Material.query.filter_by(name="Test-Material").first()
        
        assert retrieved_mat is not None
        # Da wir im Context sind, kann SQLAlchemy die Beziehung 'price_group' nachladen
        assert retrieved_mat.price_group.name == "Test-Gruppe"

def test_materials_pages_unauthorized(client):
    """
    Test-ID: QUAL-01.4
    Prüft, ob nicht-authentifizierte Nutzer zur Login-Seite weitergeleitet werden.
    """
    response = client.get('/materials/', follow_redirects=True)
    assert response.status_code == 200
    assert b"Bitte melden Sie sich an" in response.data