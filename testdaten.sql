BEGIN TRANSACTION;

-- Preisgruppen einfügen
INSERT INTO price_groups (id, name, price_per_kg) VALUES
(1, 'Standard', 19.90),
(2, 'Premium', 49.50),
(3, 'Spezial', 99.00);

-- Materialien einfügen (mit 'unit'-Spalte)
INSERT INTO materials (id, name, description, price_group_id, reorder_threshold_grams, unit) VALUES
(1, 'Acrylperlen Bunt Mix', 'Standard-Acrylperlen für Kinder und Einsteiger.', 1, 100.0, 'g'),
(2, 'Böhmische Glasperlen', 'Hochwertige, geschliffene Glasperlen aus Tschechien.', 2, 50.0, 'g'),
(3, 'Amethyst-Splitter', 'Echte Halbedelstein-Splitter zum Auffädeln.', 3, 20.0, 'g');

-- Boxen einfügen und Materialien zuweisen
INSERT INTO boxes (rfid_uid, material_id, tare_weight, stock_grams, location) VALUES
('RFID-BOX-001', 1, 25.5, 500.0, 'Regal A, Fach 1'),
('RFID-BOX-002', 2, 28.0, 350.0, 'Regal A, Fach 2'),
('RFID-BOX-003', 3, 22.1, 150.5, 'Regal B, Fach 1');

-- Kunden einfügen (mit 'role'-Spalte)
INSERT INTO customers (first_name, last_name, rfid_uid, balance, birthday, street, zip_code, city, role) VALUES
('Max', 'Mustermann', 'RFID-CUST-MAX', 25.50, '1990-05-15', 'Musterstraße 1', '97070', 'Würzburg', 'customer'),
('Erika', 'Musterfrau', 'RFID-CUST-ERIKA', 50.00, '1985-11-22', 'Testweg 5a', '97222', 'Rimpar', 'customer');

COMMIT;