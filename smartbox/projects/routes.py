from flask import render_template, redirect, url_for, flash, Blueprint, request
from smartbox import db
from smartbox.models import Project, ProjectItem, Material
from smartbox.projects.forms import ProjectForm, ProjectItemForm
from flask_login import login_required
from smartbox.decorators import admin_required
from flask_babel import _

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/')
@login_required
@admin_required
def list_all():
    projects = Project.query.order_by(Project.name).all()
    return render_template('projects/list.html', projects=projects, title=_('Projekte & Aufträge'))

@projects_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    form = ProjectForm()
    # Material-Auswahl für die Unterformulare vorbereiten
    materials = [(m.id, m.name) for m in Material.query.order_by('name').all()]
    for item_form in form.items:
        item_form.material_id.choices = materials
        
    if form.validate_on_submit():
        new_project = Project(
            name=form.name.data,
            description=form.description.data,
            image_url=form.image_url.data
        )
        for item_data in form.items.data:
            if item_data['material_id']:
                item = ProjectItem(
                    material_id=item_data['material_id'],
                    required_grams=item_data['required_grams']
                )
                new_project.items.append(item)
        
        db.session.add(new_project)
        db.session.commit()
        flash(_('Neues Projekt wurde erfolgreich angelegt.'), 'success')
        return redirect(url_for('projects.list_all'))
        
    return render_template('projects/form.html', form=form, title=_('Neues Projekt anlegen'))

# Detailansicht und Edit-Funktion können hier analog hinzugefügt werden