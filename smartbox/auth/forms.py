from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    email = StringField(_l('E-Mail'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Passwort'), validators=[DataRequired()])
    submit = SubmitField(_l('Anmelden'))