from flask import render_template, redirect, url_for, flash, Blueprint, request
from smartbox import db
from smartbox.models import Customer
from smartbox.customers.forms import CustomerForm
from flask_babel import _
from datetime import datetime
from smartbox.decorators import admin_required
from flask_login import login_required

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

    if form.validate_on_submit(): # POST-Request (Speichern)
        form.populate_obj(customer)
        # Datumsobjekt vom Formular in String für die DB umwandeln
        if customer.birthday:
            customer.birthday = customer.birthday.strftime('%Y-%m-%d')
            
        db.session.add(customer)
        db.session.commit()
        flash(_('Kundendaten wurden aktualisiert.'), 'success')
        return redirect(url_for('customers.list_all'))

    elif request.method == 'GET': # GET-Request (Seite laden)
        # Daten aus dem DB-Objekt ins Formular laden
        form.process(obj=customer)
        # String aus der DB explizit in Datumsobjekt für das Formularfeld umwandeln
        if customer.birthday:
            form.birthday.data = datetime.strptime(customer.birthday, '%Y-%m-%d').date()
    
    return render_template('customers/form.html', form=form, title=_('Kunde bearbeiten'))