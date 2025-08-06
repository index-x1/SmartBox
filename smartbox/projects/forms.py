from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField, HiddenField, FloatField, SelectField
from wtforms.validators import DataRequired, Optional, NumberRange
from flask_babel import lazy_gettext as _l

class ProjectItemForm(FlaskForm):
    """Formular für eine einzelne Material-Position in einem Projekt."""
    id = HiddenField()
    material_id = SelectField(_l('Material'), coerce=int, validators=[DataRequired()])
    required_grams = FloatField(_l('Benötigte Menge (g)'), validators=[DataRequired(), NumberRange(min=0.1)])

class ProjectForm(FlaskForm):
    """Hauptformular für ein Projekt."""
    name = StringField(_l('Projektname'), validators=[DataRequired()])
    description = TextAreaField(_l('Beschreibung'), validators=[Optional()])
    image_url = StringField(_l('Bild-URL'), validators=[Optional()])
    items = FieldList(FormField(ProjectItemForm), min_entries=1)
    submit = SubmitField(_l('Projekt speichern'))