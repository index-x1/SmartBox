from flask import render_template, redirect, url_for, flash, Blueprint
from smartbox import db
from smartbox.models import Customer
from smartbox.auth.forms import LoginForm
from flask_login import login_user, logout_user, login_required
from flask_babel import _

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Ungültige E-Mail oder Passwort.'), 'danger')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template('auth/login.html', form=form, title=_('Login'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))