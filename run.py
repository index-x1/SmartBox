from smartbox import create_app, db
from smartbox.models import Customer # Beispiel-Import

app = create_app()

# Dieser Kontext ist n�tzlich f�r die Flask-Shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Customer': Customer}