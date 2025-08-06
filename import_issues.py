import csv
import json
import os
import requests
import time

# --- KONFIGURATION ---
GITHUB_TOKEN = ""  # Ersetze dies durch dein Token
REPO_OWNER = "index-x1"  # Dein GitHub-Benutzername
REPO_NAME = "SmartBox"    # Der Name deines Repositories
CSV_FILE = "smartbox-backlog.csv" # Der Name deiner CSV-Datei

# --- SKRIPT ---
def get_existing_issues(session):
    """Holt alle existierenden Issue-Titel aus dem Repository."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    existing_titles = set()
    page = 1
    while True:
        try:
            response = session.get(url, params={'page': page, 'per_page': 100, 'state': 'all'})
            response.raise_for_status()
            issues = response.json()
            if not issues:
                break
            for issue in issues:
                existing_titles.add(issue['title'])
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ Fehler beim Abrufen der Issues: {e}")
            return None
    print(f"✅ {len(existing_titles)} existierende Issues gefunden.")
    return existing_titles

def create_github_issue(session, title, body, labels):
    """Erstellt ein einzelnes Issue, falls es noch nicht existiert."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    label_list = [label.strip() for label in labels.split(',')]
    
    issue_data = {
        "title": title,
        "body": body,
        "labels": label_list
    }
    
    try:
        response = session.post(url, data=json.dumps(issue_data))
        response.raise_for_status()
        print(f"✅ Issue '{title}' erfolgreich erstellt.")
        time.sleep(1) # Kurze Pause, um die API-Rate-Limits nicht zu überschreiten
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler beim Erstellen von Issue '{title}': {e}")
        print(f"   Antwort vom Server: {response.text}")
        return None

def main():
    if GITHUB_TOKEN == "DEIN_PERSONAL_ACCESS_TOKEN" or not GITHUB_TOKEN:
        print("Fehler: Bitte ersetze 'DEIN_PERSONAL_ACCESS_TOKEN' im Skript.")
        return

    if not os.path.exists(CSV_FILE):
        print(f"Fehler: Die Datei '{CSV_FILE}' wurde nicht gefunden.")
        return

    session = requests.Session()
    session.headers.update({
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    })

    existing_titles = get_existing_issues(session)
    if existing_titles is None:
        return

    print(f"\nLese Issues aus '{CSV_FILE}' und importiere nach '{REPO_OWNER}/{REPO_NAME}'...")
    
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row['Title']
            if title in existing_titles:
                print(f"⏩ Issue '{title}' existiert bereits und wird übersprungen.")
                continue
            create_github_issue(session, title, row['Body'], row['Labels'])

    print("\nImport abgeschlossen.")

if __name__ == "__main__":
    main()