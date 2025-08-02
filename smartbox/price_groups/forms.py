from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

class PriceGroupForm(FlaskForm):
    name = StringField(_l('Name der Preisgruppe'), validators=[DataRequired()])
    price_per_kg = DecimalField(_l('Preis pro kg (€)'), places=2, validators=[DataRequired()])
    submit = SubmitField(_l('Speichern'))