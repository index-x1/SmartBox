from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, DecimalField
from wtforms.validators import DataRequired, Optional, Email
from flask_babel import lazy_gettext as _l

class CustomerForm(FlaskForm):
    first_name = StringField(_l('Vorname'), validators=[DataRequired()])
    last_name = StringField(_l('Nachname'), validators=[DataRequired()])
    rfid_uid = StringField(_l('RFID UID'), validators=[Optional()])
    email = StringField(_l('E-Mail'), validators=[Optional(), Email()])
    phone = StringField(_l('Telefon'), validators=[Optional()])
    birthday = DateField(_l('Geburtstag'), format='%Y-%m-%d', validators=[Optional()])
    street = StringField(_l('Straße'), validators=[Optional()])
    zip_code = StringField(_l('PLZ'), validators=[Optional()])
    city = StringField(_l('Stadt'), validators=[Optional()])
    balance = DecimalField(_l('Guthaben (€)'), places=2, validators=[Optional()])
    is_active = BooleanField(_l('Aktiv'))
    submit = SubmitField(_l('Speichern'))