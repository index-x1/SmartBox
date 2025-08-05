from flask import Flask, request, current_app, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Bitte melden Sie sich an, um auf diese Seite zuzugreifen.')

def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES']) or 'de'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)
    login.init_app(app)

    app.jinja_env.globals.update(get_locale=get_locale)

    from smartbox.models import Customer
    @login.user_loader
    def load_user(id):
        # === START DEBUGGING ===
        print(f"\n--- DEBUG: User Loader ---")
        print(f"1. Gesuchte User-ID: {id} (Typ: {type(id)})")
        user = Customer.query.get(int(id))
        print(f"2. Ergebnis der DB-Abfrage: {user}")
        print(f"--------------------------\n")
        # === ENDE DEBUGGING ===
        return user

    # Blueprints registrieren
    from smartbox.customers.routes import customers_bp
    from smartbox.boxes.routes import boxes_bp
    from smartbox.price_groups.routes import price_groups_bp
    from smartbox.materials.routes import materials_bp
    from smartbox.weighing.routes import weighing_bp
    from smartbox.auth.routes import auth_bp

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(boxes_bp, url_prefix='/boxes')
    app.register_blueprint(price_groups_bp, url_prefix='/price-groups')
    app.register_blueprint(materials_bp, url_prefix='/materials')
    app.register_blueprint(weighing_bp, url_prefix='/weighing')
    app.register_blueprint(auth_bp)

    @app.route('/')
    def home():
        return render_template('home.html', title=_l('Hauptmenü'))

    @app.route('/stammdaten')
    def stammdaten_menu():
        return render_template('stammdaten_menu.html', title=_l('Stammdaten'))

    return app