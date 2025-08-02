import os

# Verzeichnis, in dem diese Datei liegt
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ein-sehr-sicherer-fallback-schluessel'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'smartbox.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['de', 'en']

#temp debug
print(f"DEBUG: Aktueller Datenbankpfad ist: {Config.SQLALCHEMY_DATABASE_URI}")
