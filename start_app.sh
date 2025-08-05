#!/bin/bash

# Wechsle in das Projektverzeichnis
cd /home/daniel/smartbox_project

# Aktiviere die virtuelle Umgebung
source venv/bin/activate

# Starte den Flask-Server auf allen Netzwerkadressen
echo "Starte SmartBox Server..."
flask run --host=0.0.0.0
