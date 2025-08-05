from smartbox import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # <-- DIESE ZEILE IST NEU UND KORRIGIERT DEN FEHLER

class Customer(UserMixin, db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    rfid_uid = db.Column(db.String(50), unique=True, index=True)
    birthday = db.Column(db.String(10), nullable=True)
    password_hash = db.Column(db.String(256), nullable=True)
    street = db.Column(db.String(150))
    zip_code = db.Column(db.String(10))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100), default='Deutschland')
    email = db.Column(db.String(120), unique=True, index=True)
    phone = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(20), default='customer', nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'

class PriceGroup(db.Model):
    __tablename__ = 'price_groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price_per_kg = db.Column(db.Numeric(10, 2), nullable=False)
    
class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    manufacturer = db.Column(db.String(100))
    manufacturer_sku = db.Column(db.String(100))  # NEU: Artikelnummer des Herstellers
    usage_hint = db.Column(db.Text)
    unit = db.Column(db.String(20), default='g', nullable=False)
    reorder_threshold_grams = db.Column(db.Float)
    grams_per_piece = db.Column(db.Float, nullable=True)
    price_group_id = db.Column(db.Integer, db.ForeignKey('price_groups.id'))
    image_url = db.Column(db.String(255))        # NEU: Bild-URL
    supplier_url_1 = db.Column(db.String(255))   # NEU: Link zu Lieferant 1
    supplier_url_2 = db.Column(db.String(255))   # NEU: Link zu Lieferant 2
    supplier_url_3 = db.Column(db.String(255))   # NEU: Link zu Lieferant 3
    tags = db.Column(db.String(200))             # NEU: Schlagworte (z.B. "perlen,holz,schmuck")
    is_active = db.Column(db.Boolean, default=True) # NEU: Um Material auszublenden

    price_group = db.relationship('PriceGroup', backref=db.backref('materials', lazy=True))

class Box(db.Model):
    __tablename__ = 'boxes'
    id = db.Column(db.Integer, primary_key=True)
    rfid_uid = db.Column(db.String(50), nullable=False, unique=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    tare_weight = db.Column(db.Float)
    location = db.Column(db.String(100))
    stock_grams = db.Column(db.Float, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    material = db.relationship('Material', backref=db.backref('boxes', lazy=True))

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    box_id = db.Column(db.Integer, db.ForeignKey('boxes.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    grams_withdrawn = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', backref=db.backref('transactions', lazy=True))
    box = db.relationship('Box', backref=db.backref('transactions', lazy=True))