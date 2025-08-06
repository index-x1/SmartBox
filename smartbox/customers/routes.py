from flask import render_template, redirect, url_for, flash, Blueprint, request
from smartbox import db
from smartbox.models import Customer, Transaction
from smartbox.customers.forms import CustomerForm
from flask_babel import _
from datetime import datetime
from smartbox.decorators import admin_required
from flask_login import login_required
from decimal import Decimal

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/')
@login_required
@admin_required
def list_all():
    customers = Customer.query.order_by(Customer.last_name).all()
    return render_template('customers/list.html', customers=customers, title=_('Kundenübersicht'))

@customers_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    form = CustomerForm()
    if request.method == 'GET':
        form.is_active.data = True
        
    if form.validate_on_submit():
        new_customer = Customer()
        # Daten vom Formular ins Model-Objekt übertragen
        form.populate_obj(new_customer)
        # Datumsobjekt explizit in String umwandeln für die DB
        if new_customer.birthday:
            new_customer.birthday = new_customer.birthday.strftime('%Y-%m-%d')
            
        db.session.add(new_customer)
        db.session.commit()
        flash(_('Kunde wurde erfolgreich angelegt.'), 'success')
        return redirect(url_for('customers.list_all'))
    return render_template('customers/form.html', form=form, title=_('Neuen Kunden anlegen'))

@customers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    customer = Customer.query.get_or_404(id)
    form = CustomerForm()

    if form.validate_on_submit():
        # Bestehende Kundendaten aktualisieren
        customer.first_name = form.first_name.data
        customer.last_name = form.last_name.data
        customer.rfid_uid = form.rfid_uid.data
        customer.email = form.email.data
        customer.phone = form.phone.data
        customer.birthday = form.birthday.data
        customer.street = form.street.data
        customer.zip_code = form.zip_code.data
        customer.city = form.city.data
        customer.is_active = form.is_active.data

        # NEU: Guthaben aufladen und Transaktion erstellen
        deposit = form.deposit_amount.data
        if deposit and deposit > 0:
            customer.balance += deposit
            
            # Transaktion protokollieren
            new_transaction = Transaction(
                customer_id=customer.id,
                transaction_type='deposit',
                cost=deposit, # Positiver Wert für Einzahlung
                status='completed'
            )
            db.session.add(new_transaction)
            flash(_(f'{deposit}€ Guthaben wurde erfolgreich hinzugefügt.'), 'success')

        db.session.commit()
        flash(_('Kundendaten wurden aktualisiert.'), 'info')
        return redirect(url_for('customers.list_all'))

    elif request.method == 'GET':
        # Formular mit den bestehenden Daten vorbefüllen
        form.process(obj=customer)
        if customer.birthday and isinstance(customer.birthday, str):
            form.birthday.data = datetime.strptime(customer.birthday, '%Y-%m-%d').date()
    
    return render_template('customers/form.html', form=form, title=_('Kunde bearbeiten'))