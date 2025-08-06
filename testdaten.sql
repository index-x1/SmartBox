BEGIN TRANSACTION;

-- Preisgruppen
INSERT INTO price_groups (id, name, price_per_kg) VALUES
(1, 'Basis', 15.00),
(2, 'Standard', 29.90),
(3, 'Premium', 59.50),
(4, 'Spezial', 120.00);

-- Materialien (KORRIGIERTE VERSION)
INSERT INTO materials (id, name, description, manufacturer, manufacturer_sku, price_group_id, image_url, supplier_url_1, tags, unit) VALUES
(1, 'Acrylperlen Bunt Mix', 'Bunte Perlenmischung aus Acryl, 6-8mm.', 'Bastel-Profi', 'AC-MIX-01', 1, '/static/images/acrylperlen.jpg', 'https://shop1.example.com/acrylperlen', 'perlen,kunststoff,bunt', 'g'),
(2, 'Holzknöpfe Natur', '20mm Holzknöpfe aus Buchenholz, 2-Loch.', 'Holz-Wurm', 'HK-BU-20-2', 2, '/static/images/holzknopf.jpg', 'https://shop2.example.com/holzknopf', 'knöpfe,holz,natur', 'g'),
(3, 'Böhmische Glasperlen Blau', 'Hochwertige, geschliffene Glasperlen aus Tschechien, 4mm.', 'Glas & Co', 'GL-BOH-BL-4', 3, '/static/images/glasperlen.jpg', 'https://shop1.example.com/glasperlen', 'perlen,glas,schmuck,blau', 'g'),
(4, 'Silberdraht 0.4mm', 'Reiner Silberdraht für Schmuckherstellung.', 'Edelmetall AG', 'AG-DR-04', 4, '/static/images/silberdraht.jpg', 'https://shop3.example.com/silberdraht', 'draht,silber,schmuck', 'g'),
(5, 'Merinowolle Filz Grün', 'Weicher Filz aus 100% Merinowolle.', 'Woll-Manufaktur', 'MW-FI-GR', 2, '/static/images/filz.jpg', 'https://shop2.example.com/filz', 'wolle,filz,textil,grün', 'g');

-- Boxen
INSERT INTO boxes (id, rfid_uid, material_id, tare_weight, stock_grams, location) VALUES
(1, 'RFID-BOX-001', 1, 25.5, 510.0, 'Regal A, Fach 1'),
(2, 'RFID-BOX-002', 2, 28.0, 355.0, 'Regal A, Fach 2'),
(3, 'RFID-BOX-003', 3, 22.1, 150.5, 'Regal B, Fach 1'),
(4, 'RFID-BOX-004', 4, 15.0, 80.0, 'Wertschrank'),
(5, 'RFID-BOX-005', 5, 30.0, 420.0, 'Regal C, Fach 3');

-- Kunden (mit gehashtem Admin-Passwort für 'admin')
INSERT INTO customers (id, first_name, last_name, rfid_uid, balance, birthday, role, email, is_active, password_hash) VALUES
(1, 'Max', 'Mustermann', 'RFID-CUST-MAX', 25.50, '1990-05-15', 'customer', 'max@test.de', 1, NULL),
(2, 'Erika', 'Musterfrau', 'RFID-CUST-ERIKA', 50.00, '1985-11-22', 'customer', 'erika@test.de', 1, NULL),
(3, 'Admin', 'User', 'RFID-ADMIN-001', 999.00, '1980-01-01', 'admin', 'admin@smartbox.de', 1, 'scrypt:32768:8:1$ET8FnpzQmXIJsPKA$433377aa61363e53fc480734873be1c07a037424b4ad875adb79db0786f90442691e79d62ef5ddde6e22d529eef466be33bd7d992e515444ed373190cc1bcf54'), -- Ersetze dies durch einen echten Hash
(4, 'Lisa', 'Kreativ', 'RFID-CUST-LISA', 15.00, '2001-07-30', 'customer', 'lisa@test.de', 1, NULL),
(5, 'Tom', 'Bastler', 'RFID-CUST-TOM', 5.20, '1995-03-12', 'customer', 'tom@test.de', 0, NULL);

-- Projekte
INSERT INTO projects (id, name, description, image_url) VALUES
(1, 'Schmuck-Set Amethyst', 'Ein einfaches Set zur Herstellung einer Halskette und eines Armbands.', '/static/images/projekt_schmuck.jpg'),
(2, 'Vogelhaus-Bausatz', 'Alle benötigten Holzteile und Schrauben für ein kleines Vogelhaus.', '/static/images/projekt_vogelhaus.jpg');

-- Projekt-Positionen (BOM)
INSERT INTO project_items (project_id, material_id, required_grams, picking_order) VALUES
(1, 3, 50, 1),  -- 50g Amethyst-Splitter
(1, 4, 5, 2),   -- 5g Silberdraht
(2, 2, 20, 1);  -- 20g Holzknöpfe (als symbolische Schrauben)

COMMIT;