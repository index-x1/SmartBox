from flask import render_template, redirect, url_for, flash, Blueprint
from smartbox import db
from smartbox.models import PriceGroup
from smartbox.price_groups.forms import PriceGroupForm
from flask_babel import _

price_groups_bp = Blueprint('price_groups', __name__, template_folder='../templates/price_groups')

@price_groups_bp.route('/')
def list_all():
    groups = PriceGroup.query.order_by(PriceGroup.name).all()
    return render_template('price_groups/list.html', groups=groups, title=_('Preisgruppen'))

@price_groups_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = PriceGroupForm()
    if form.validate_on_submit():
        new_group = PriceGroup(
            name=form.name.data,
            price_per_kg=form.price_per_kg.data
        )
        db.session.add(new_group)
        db.session.commit()
        flash(_('Preisgruppe wurde erfolgreich angelegt.'), 'success')
        return redirect(url_for('price_groups.list_all'))
    return render_template('price_groups/form.html', form=form, title=_('Neue Preisgruppe anlegen'))

@price_groups_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    group = PriceGroup.query.get_or_404(id)
    form = PriceGroupForm(obj=group)
    if form.validate_on_submit():
        group.name = form.name.data
        group.price_per_kg = form.price_per_kg.data
        db.session.commit()
        flash(_('Preisgruppe wurde aktualisiert.'), 'success')
        return redirect(url_for('price_groups.list_all'))
    return render_template('price_groups/form.html', form=form, title=_('Preisgruppe bearbeiten'))