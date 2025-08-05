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

-- Kunden
INSERT INTO customers (id, first_name, last_name, rfid_uid, balance, birthday, street, zip_code, city, role, email, is_active) VALUES
(1, 'Max', 'Mustermann', 'RFID-CUST-MAX', 25.50, '1990-05-15', 'Musterstraße 1', '97070', 'Würzburg', 'customer', 'max@test.de', 1),
(2, 'Erika', 'Musterfrau', 'RFID-CUST-ERIKA', 50.00, '1985-11-22', 'Testweg 5a', '97222', 'Rimpar', 'customer', 'erika@test.de', 1),
(3, 'Admin', 'User', 'RFID-ADMIN-001', 999.00, '1980-01-01', 'Hauptstr. 10', '10115', 'Berlin', 'admin', 'admin@smartbox.de', 1),
(4, 'Lisa', 'Kreativ', 'RFID-CUST-LISA', 15.00, '2001-07-30', 'Am Park 3', '97072', 'Würzburg', 'customer', 'lisa@test.de', 1),
(5, 'Tom', 'Bastler', 'RFID-CUST-TOM', 5.20, '1995-03-12', 'Werkstattweg 8', '97292', 'Zell', 'customer', 'tom@test.de', 0);

COMMIT;