from flask import Flask, request, current_app, render_template # render_template hier importieren
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babel import Babel, lazy_gettext as _l

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()

# Die Funktion zur Sprachauswahl
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Erweiterungen mit der App initialisieren
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app, locale_selector=get_locale)

    # Mache die get_locale Funktion im Template verf�gbar
    app.jinja_env.globals.update(get_locale=get_locale)

    # Blueprints registrieren
    from smartbox.customers.routes import customers_bp
    from smartbox.boxes.routes import boxes_bp
    from smartbox.price_groups.routes import price_groups_bp
    from smartbox.materials.routes import materials_bp
    from smartbox.weighing.routes import weighing_bp

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(boxes_bp, url_prefix='/boxes')
    app.register_blueprint(price_groups_bp, url_prefix='/price-groups')
    app.register_blueprint(materials_bp, url_prefix='/materials')
    app.register_blueprint(weighing_bp, url_prefix='/weighing')

    # Haupt-Route
    @app.route('/')
    def home():
        return render_template('home.html', title=_l('Hauptmenü'))

    # NEUE ROUTE HINZUFÜGEN
    @app.route('/stammdaten')
    def stammdaten_menu():
        return render_template('stammdaten_menu.html', title=_l('Stammdaten'))

    return app