from flask import render_template, redirect, url_for, flash, Blueprint
from smartbox import db
from smartbox.models import Material, PriceGroup
from smartbox.materials.forms import MaterialForm
from flask_babel import _
from smartbox.decorators import admin_required
from flask_login import login_required

# KORREKTUR: template_folder entfernen
materials_bp = Blueprint('materials', __name__)

@materials_bp.route('/')
@login_required
@admin_required
def list_all():
    materials = Material.query.order_by(Material.name).all()
    # KORREKTUR: Expliziter Pfad zum Template
    return render_template('materials/list.html', materials=materials, title=_('Materialien'))

@materials_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    form = MaterialForm()
    form.price_group_id.choices = [(g.id, g.name) for g in PriceGroup.query.order_by('name').all()]

    if form.validate_on_submit():
        new_material = Material()
        form.populate_obj(new_material)
        db.session.add(new_material)
        db.session.commit()
        flash(_('Material wurde erfolgreich angelegt.'), 'success')
        return redirect(url_for('materials.list_all'))
    # KORREKTUR: Expliziter Pfad zum Template
    return render_template('materials/form.html', form=form, title=_('Neues Material anlegen'))

@materials_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(id):
    material = Material.query.get_or_404(id)
    form = MaterialForm(obj=material)
    form.price_group_id.choices = [(g.id, g.name) for g in PriceGroup.query.order_by('name').all()]

    if form.validate_on_submit():
        form.populate_obj(material)
        db.session.commit()
        flash(_('Materialdaten wurden aktualisiert.'), 'success')
        return redirect(url_for('materials.list_all'))
    # KORREKTUR: Expliziter Pfad zum Template
    return render_template('materials/form.html', form=form, title=_('Material bearbeiten'))