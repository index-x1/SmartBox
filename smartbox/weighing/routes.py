from flask import render_template, Blueprint, jsonify, request, session
from smartbox import db
from smartbox.models import Customer, Box, Transaction, PriceGroup, Material
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
    session['state'] = 'AWAITING_BOX'
    
    return jsonify({
        'status': 'ok',
        'customer': { 'firstName': customer.first_name, 'rfid': customer.rfid_uid, 'balance': float(customer.balance) },
        'next_step': 'AWAITING_BOX'
    })

@weighing_bp.route('/api/session/scan_box', methods=['POST'])
def api_scan_box():
    if session.get('state') != 'AWAITING_BOX':
        return jsonify({'status': 'error', 'message': 'Falscher Prozess-Schritt.'}), 400

    box_rfid = request.json.get('box_rfid')
    box = Box.query.filter_by(rfid_uid=box_rfid).first()
    if not box or not box.is_active or not box.material:
        return jsonify({'status': 'error', 'message': 'Box nicht gefunden oder kein Material zugewiesen.'}), 404

    # === START: Intelligente Tara-Prüfung ===
    measured_weight = float(request.json.get('weight_before', box.stock_grams or 500.0))
    db_weight = box.stock_grams or 0.0

    # Toleranz dynamisch bestimmen (z.B. 3% vom Materialgewicht, aber mind. 2g)
    tolerance_percent = 3.0 
    tolerance_grams = max(2.0, db_weight * (tolerance_percent / 100.0))
    
    deviation = abs(measured_weight - db_weight)

    if deviation > tolerance_grams:
        # Logge den Vorfall für spätere Analyse
        # db.session.add(HardwareEvent(box_id=box.id, ...))
        # db.session.commit()
        print(f"ALARM: Starke Tara-Abweichung bei Box {box.rfid_uid}. Gemessen: {measured_weight}g, DB: {db_weight}g")
        return jsonify({
            'status': 'error', 
            'message': f'Gewichtsabweichung zu groß ({deviation:.1f}g). Bitte Personal kontaktieren.'
        }), 409 # 409 Conflict: Der Zustand der Ressource ist unerwartet

    # === ENDE: Intelligente Tara-Prüfung ===

    session['state'] = 'WITHDRAWAL'
    session['box_id'] = box.id
    session['initial_weight'] = measured_weight

    return jsonify({
        'status': 'ok',
        'box': { 'name': box.material.name, 'price_per_kg': float(box.material.price_group.price_per_kg) },
        'next_step': 'WITHDRAWAL'
    })

@weighing_bp.route('/api/session/confirm', methods=['POST'])
def api_confirm():
    if session.get('state') != 'WITHDRAWAL':
        return jsonify({'status': 'error', 'message': 'Falscher Prozess-Schritt.'}), 400

    customer_id = session.get('customer_id')
    box_id = session.get('box_id')
    initial_weight = session.get('initial_weight')

    customer = db.session.get(Customer, customer_id)
    box = db.session.get(Box, box_id)

    final_weight = float(request.json.get('weight_after', initial_weight - 52.0))
    withdrawn_grams = initial_weight - final_weight

    # === START: Plausibilitäts-Checks nach Entnahme ===
    if final_weight > initial_weight:
        print(f"ALARM: Gewicht hat bei Box {box.rfid_uid} zugenommen! Manipulation?")
        return jsonify({'status': 'error', 'message': 'Unerwartete Gewichtszunahme. Vorgang abgebrochen.'}), 400

    if withdrawn_grams <= 0.5: # Mindestentnahme, um "Wackeln" abzufangen
        session['state'] = 'AWAITING_BOX'
        return jsonify({'status': 'ok', 'next_step': 'AWAITING_BOX', 'message': 'Keine nennenswerte Entnahme erkannt.'})
    # === ENDE: Plausibilitäts-Checks ===
    
    price_per_gram = Decimal(box.material.price_group.price_per_kg) / Decimal(1000)
    cost = Decimal(withdrawn_grams) * price_per_gram

    if customer.balance < cost:
        # Berechnen, wie viel der Kunde sich leisten kann
        affordable_grams = customer.balance / price_per_gram
        grams_to_put_back = withdrawn_grams - float(affordable_grams)

        message = f"Guthaben reicht nicht aus. Bitte lege {grams_to_put_back:.1f}g zurück."

        # Stückgut-Logik
        grams_per_piece = box.material.grams_per_piece
        if grams_per_piece and grams_per_piece > 0:
            affordable_pieces = int(affordable_grams / Decimal(grams_per_piece))
            pieces_to_put_back = round(grams_to_put_back / grams_per_piece)
            message = f"Guthaben reicht nur für {affordable_pieces} Stück. Bitte lege {pieces_to_put_back} Stück zurück."

        return jsonify({'status': 'error', 'message': message, 'error_code': 'INSUFFICIENT_FUNDS'}), 402

    customer.balance -= cost
    box.stock_grams = final_weight
    
    new_transaction = Transaction(
        customer_id=customer_id, box_id=box_id, material_id=box.material_id,
        grams_withdrawn=withdrawn_grams, cost=cost, timestamp=datetime.utcnow()
    )
    
    db.session.add(new_transaction)
    db.session.commit()

    # Automatisches Tara-Update bei kleiner Abweichung
    if abs(box.tare_weight - final_weight) < 5.0 and box.stock_grams < 10.0: # Beispiel-Logik für leere Box
        box.tare_weight = final_weight
        db.session.commit()
        print(f"INFO: Tara-Gewicht für Box {box.rfid_uid} auf {final_weight}g neu kalibriert.")

    session['state'] = 'AWAITING_BOX'
    
    return jsonify({
        'status': 'ok',
        'transaction': { 'name': box.material.name, 'amount': round(withdrawn_grams, 2), 'price': round(cost, 2) },
        'new_balance': float(customer.balance),
        'next_step': 'AWAITING_BOX'
    })