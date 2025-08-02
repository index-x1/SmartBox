from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FloatField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_babel import lazy_gettext as _l

class BoxForm(FlaskForm):
    rfid_uid = StringField(_l('RFID UID'), validators=[DataRequired()])
    material_id = SelectField(_l('Material'), coerce=int, validators=[DataRequired()])
    tare_weight = FloatField(_l('Leergewicht (g)'), validators=[Optional()])
    location = StringField(_l('Lagerort'), validators=[Optional()])
    is_active = BooleanField(_l('Aktiv'))
    submit = SubmitField(_l('Speichern'))