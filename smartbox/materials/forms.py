from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Optional
from flask_babel import lazy_gettext as _l

class MaterialForm(FlaskForm):
    name = StringField(_l('Materialname'), validators=[DataRequired()])
    description = TextAreaField(_l('Beschreibung'), validators=[Optional()])
    manufacturer = StringField(_l('Hersteller'), validators=[Optional()])
    usage_hint = TextAreaField(_l('Verwendungshinweis'), validators=[Optional()])
    price_group_id = SelectField(_l('Preisgruppe'), coerce=int, validators=[DataRequired()])
    reorder_threshold_grams = FloatField(_l('Mindestbestand (g)'), validators=[Optional()])
    grams_per_piece = FloatField(_l('Gewicht pro Stück (g)'), validators=[Optional()])
    submit = SubmitField(_l('Speichern'))