from flask import render_template, redirect, url_for, flash, Blueprint
from smartbox import db
from smartbox.models import Material, PriceGroup
from smartbox.materials.forms import MaterialForm
from flask_babel import _
from smartbox.decorators import admin_required

materials_bp = Blueprint('materials', __name__, template_folder='../templates/materials')

@materials_bp.route('/')
def list_all():
    materials = Material.query.order_by(Material.name).all()
    return render_template('materials/list.html', materials=materials, title=_('Materialien'))

@materials_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = MaterialForm()
    form.price_group_id.choices = [(g.id, g.name) for g in PriceGroup.query.order_by('name').all()]

    if form.validate_on_submit():
        new_material = Material(
            name=form.name.data,
            description=form.description.data,
            manufacturer=form.manufacturer.data,
            usage_hint=form.usage_hint.data,
            price_group_id=form.price_group_id.data,
            reorder_threshold_grams=form.reorder_threshold_grams.data
        )
        db.session.add(new_material)
        db.session.commit()
        flash(_('Material wurde erfolgreich angelegt.'), 'success')
        return redirect(url_for('materials.list_all'))
    return render_template('materials/form.html', form=form, title=_('Neues Material anlegen'))

@materials_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    material = Material.query.get_or_404(id)
    form = MaterialForm(obj=material)
    form.price_group_id.choices = [(g.id, g.name) for g in PriceGroup.query.order_by('name').all()]

    if form.validate_on_submit():
        material.name = form.name.data
        material.description = form.description.data
        material.manufacturer = form.manufacturer.data
        material.usage_hint = form.usage_hint.data
        material.price_group_id = form.price_group_id.data
        material.reorder_threshold_grams = form.reorder_threshold_grams.data
        db.session.commit()
        flash(_('Materialdaten wurden aktualisiert.'), 'success')
        return redirect(url_for('materials.list_all'))
    return render_template('materials/form.html', form=form, title=_('Material bearbeiten'))