from smartbox.models import Customer, Material

# === Unit-Test für das Customer Model ===
def test_password_hashing(new_customer):
    """
    Test-ID: QUAL-01.6
    Prüft die Passwort-Methoden des Customer-Models.
    """
    assert new_customer.password_hash != 'password123'
    assert new_customer.check_password('password123')
    assert not new_customer.check_password('wrongpassword')


# === Unit-Tests für das Material Model ===
def test_material_needs_reorder():
    """
    Test-ID: QUAL-01.7
    Prüft die Logik für den Nachbestell-Bedarf.
    """
    material = Material(name="Test Material", reorder_threshold_grams=100.0)
    
    # Fall 1: Bestand ist über dem Schwellenwert
    assert not material.needs_reorder(current_stock=150.0)
    
    # Fall 2: Bestand ist genau auf dem Schwellenwert
    assert not material.needs_reorder(current_stock=100.0)
    
    # Fall 3: Bestand ist unter dem Schwellenwert
    assert material.needs_reorder(current_stock=99.9)

def test_material_reorder_with_no_threshold():
    """
    Test-ID: QUAL-01.8
    Prüft das Verhalten, wenn kein Schwellenwert gesetzt ist.
    """
    material_no_threshold = Material(name="No Threshold Material")
    assert not material_no_threshold.needs_reorder(current_stock=10.0)