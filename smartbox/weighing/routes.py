from flask import render_template, Blueprint, jsonify, request, session
from smartbox import db
from smartbox.models import Customer, Box, Transaction, Project
from flask_login import login_required
from flask_babel import _
from datetime import datetime
from decimal import Decimal, getcontext

# Setzt die Präzision für Decimal-Berechnungen
getcontext().prec = 10

weighing_bp = Blueprint('weighing', __name__)

@weighing_bp.route('/session')
def session_view():
    session.clear()
    return render_template('weighing/session.html', title=_('Kundenmodus'))

# --- API Routen ---

@weighing_bp.route('/api/session/login', methods=['POST'])
def api_login():
    rfid = request.json.get('rfid_uid')
    customer = Customer.query.filter_by(rfid_uid=rfid).first()
    if not customer or not customer.is_active:
        return jsonify({'status': 'error', 'message': 'Kunde nicht gefunden oder inaktiv.'}), 404
    
    session['customer_id'] = customer.id
    return jsonify({
        'status': 'ok',
        'customer': { 'firstName': customer.first_name, 'balance': float(customer.balance) }
    })

@weighing_bp.route('/api/projects', methods=['POST'])
@login_required
def api_get_projects():
    projects = Project.query.order_by(Project.name).all()
    projects_data = [{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'image_url': p.image_url
    } for p in projects]
    return jsonify({'status': 'ok', 'projects': projects_data})

@weighing_bp.route('/api/project/<int:project_id>', methods=['POST'])
@login_required
def api_get_project_details(project_id):
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({'status': 'error', 'message': 'Projekt nicht gefunden.'}), 404

    items_data = [{
        'material_name': item.material.name,
        'material_id': item.material.id,
        'box_rfid': item.material.boxes[0].rfid_uid if item.material.boxes else None, # Nimmt die erste verknüpfte Box
        'location': item.material.boxes[0].location if item.material.boxes else 'N/A',
        'required_grams': item.required_grams
    } for item in project.items.order_by('picking_order')]
    
    return jsonify({
        'status': 'ok',
        'project': {
            'id': project.id,
            'name': project.name,
            'items': items_data
        }
    })

@weighing_bp.route('/api/session/scan_box', methods=['POST'])
def api_scan_box():
    if session.get('state') != 'AWAITING_BOX':
        return jsonify({'status': 'error', 'message': 'Falscher Prozess-Schritt.'}), 400

    box_rfid = request.json.get('box_rfid')
    box = Box.query.filter_by(rfid_uid=box_rfid).first()
    if not box or not box.is_active or not box.material:
        return jsonify({'status': 'error', 'message': 'Box nicht gefunden oder kein Material zugewiesen.'}), 404

    initial_weight = float(request.json.get('weight_before', box.stock_grams or 500.0))
    # ... (Tara-Prüfung von vorher bleibt hier) ...

    session['state'] = 'WITHDRAWAL'
    session['box_id'] = box.id
    session['initial_weight'] = initial_weight

    # NEU: Mehr Details an das Frontend senden
    return jsonify({
        'status': 'ok',
        'box': {
            'name': box.material.name,
            'description': box.material.description,
            'usage_hint': box.material.usage_hint,
            'image_url': box.material.image_url
        },
        'next_step': 'WITHDRAWAL'
    })

@weighing_bp.route('/api/session/confirm', methods=['POST'])
def api_confirm():
    if session.get('state') != 'WITHDRAWAL':
        return jsonify({'status': 'error', 'message': 'Falscher Prozess-Schritt.'}), 400

    # Daten aus der Session laden
    customer_id = session.get('customer_id')
    box_id = session.get('box_id')
    initial_weight = session.get('initial_weight')

    customer = db.session.get(Customer, customer_id)
    box = db.session.get(Box, box_id)

    # Simuliertes finales Gewicht aus dem Frontend
    final_weight = float(request.json.get('weight_after', initial_weight - 52.0))
    withdrawn_grams = initial_weight - final_weight

    # --- Plausibilitäts-Checks ---
    if final_weight > initial_weight:
        # Manipulation / Fehler: Protokolliere den Vorfall
        failed_transaction = Transaction(
            customer_id=customer_id, box_id=box_id, material_id=box.material_id,
            transaction_type='withdrawal', initial_grams=initial_weight,
            final_grams=final_weight, grams_withdrawn=withdrawn_grams,
            cost=0, status='failed_weight_increase'
        )
        db.session.add(failed_transaction)
        db.session.commit()
        return jsonify({'status': 'error', 'message': 'Unerwartete Gewichtszunahme.'}), 400

    if withdrawn_grams <= 0.5:
        session['state'] = 'AWAITING_BOX'
        return jsonify({'status': 'ok', 'next_step': 'AWAITING_BOX', 'message': 'Keine Entnahme erkannt.'})

    price_per_gram = Decimal(box.material.price_group.price_per_kg) / Decimal(1000)
    cost = Decimal(withdrawn_grams) * price_per_gram

    # --- Prüfung auf ausreichendes Guthaben ---
    if customer.balance < cost:
        # Transaktion als fehlgeschlagen protokollieren
        failed_transaction = Transaction(
            customer_id=customer_id, box_id=box_id, material_id=box.material_id,
            transaction_type='withdrawal', initial_grams=initial_weight,
            final_grams=final_weight, grams_withdrawn=withdrawn_grams,
            cost=cost, status='failed_insufficient_funds'
        )
        db.session.add(failed_transaction)
        db.session.commit()
        # Detaillierte Fehlermeldung
        affordable_grams = customer.balance / price_per_gram
        grams_to_put_back = withdrawn_grams - float(affordable_grams)
        message = f"Guthaben reicht nicht aus. Bitte lege {grams_to_put_back:.1f}g zurück."
        return jsonify({'status': 'error', 'message': message, 'error_code': 'INSUFFICIENT_FUNDS'}), 402

    # --- Erfolgreiche Transaktion durchführen ---
    customer.balance -= cost
    box.stock_grams = final_weight
    
    new_transaction = Transaction(
        customer_id=customer_id,
        box_id=box_id,
        material_id=box.material_id,
        transaction_type='withdrawal',
        initial_grams=initial_weight,
        final_grams=final_weight,
        grams_withdrawn=withdrawn_grams,
        cost=cost,
        status='completed'
    )
    
    db.session.add(new_transaction)
    db.session.commit()

    session['state'] = 'AWAITING_BOX'
    
    return jsonify({
        'status': 'ok',
        'transaction': { 'name': box.material.name, 'amount': round(withdrawn_grams, 2), 'price': float(cost) },
        'new_balance': float(customer.balance),
        'next_step': 'AWAITING_BOX'
    })