from flask import render_template, redirect, url_for, flash, Blueprint
from smartbox import db
from smartbox.models import Box, Material
from smartbox.boxes.forms import BoxForm
from flask_babel import _
from flask_login import login_required
from smartbox.decorators import admin_required

# Wir entfernen den 'template_folder', um die globalen Templates zu nutzen
boxes_bp = Blueprint('boxes', __name__)

@boxes_bp.route('/')
@login_required 
@admin_required
def list_all():
    boxes = Box.query.all()
    # Wir geben den exakten Pfad zum Template an
    return render_template('boxes/list.html', boxes=boxes, title=_('Boxenübersicht'))

@boxes_bp.route('/add', methods=['GET', 'POST'])
@login_required 
@admin_required
def add():
    form = BoxForm()
    form.material_id.choices = [(m.id, m.name) for m in Material.query.order_by('name').all()]

    if form.validate_on_submit():
        new_box = Box(
            rfid_uid=form.rfid_uid.data,
            material_id=form.material_id.data,
            tare_weight=form.tare_weight.data,
            location=form.location.data,
            is_active=form.is_active.data
        )
        db.session.add(new_box)
        db.session.commit()
        flash(_('Box wurde erfolgreich angelegt.'), 'success')
        return redirect(url_for('boxes.list_all'))
    # Wir geben den exakten Pfad zum Template an
    return render_template('boxes/form.html', form=form, title=_('Neue Box anlegen'))

@boxes_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required 
@admin_required
def edit(id):
    box = Box.query.get_or_404(id)
    form = BoxForm(obj=box)
    form.material_id.choices = [(m.id, m.name) for m in Material.query.order_by('name').all()]

    if form.validate_on_submit():
        box.rfid_uid = form.rfid_uid.data
        box.material_id = form.material_id.data
        box.tare_weight = form.tare_weight.data
        box.location = form.location.data
        box.is_active = form.is_active.data
        db.session.commit()
        flash(_('Boxdaten wurden aktualisiert.'), 'success')
        return redirect(url_for('boxes.list_all'))
    # Wir geben den exakten Pfad zum Template an
    return render_template('boxes/form.html', form=form, title=_('Box bearbeiten'))