from smartbox.models import Customer

# === Integrationstest ===
def test_home_page_loads(client):
    """
    Test-ID: QUAL-01.1
    Prüft, ob die Hauptseite ('/') erfolgreich geladen wird (Status Code 200).
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Willkommen im SmartBox System" in response.data
