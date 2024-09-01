# Anleitung zur Bereitstellung einer Flask-Anwendung mit Google Cloud

## Voraussetzungen

Bevor wir mit dem Deployment beginnen, stelle sicher, dass du die folgenden Voraussetzungen erfüllst:

1. **Google Cloud Konto**: Stelle sicher, dass du ein Google Cloud Konto besitzt. Falls du noch keins hast, registriere dich auf [Google Cloud](https://cloud.google.com/) und nutze den kostenlosen Testzeitraum.
2. **Python**: Stelle sicher, dass Python installiert ist. Flask erfordert Python 3.7 oder höher.
3. **Google Cloud SDK**: Installiere das [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
4. **Flask-Anwendung**: Eine bereits funktionierende Flask-Anwendung.

## 1. Erstellen der Flask-Anwendung

Beginne mit dem Erstellen einer Flask-Anwendung. Hierbei ist es wichtig, Frontend und Backend strikt zu trennen, sodass das Frontend später unabhängig vom Backend online bereitgestellt werden kann.

### 1.1 Projektstruktur

Strukturiere deine Anwendung wie folgt:

```plaintext
my-flask-app/
├── app.py             # Hauptdatei der Flask-Anwendung
├── templates/         # HTML-Dateien für das Frontend
│   └── index.html
├── static/            # Statische Dateien wie CSS, JS, Bilder
│   ├── styles.css
│   └── script.js
├── config.js          # Konfigurationsdatei für das Frontend
├── requirements.txt   # Liste der Python-Abhängigkeiten
└── app.yaml           # Konfigurationsdatei für Google App Engine 
```


### 1.2 Inhalt der app.py
In der app.py wird die eigentliche Flask-Anwendung definiert:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### 1.3 requirements.txt
Erstelle eine requirements.txt, um die Abhängigkeiten deiner Flask-App zu verwalten:

```plaintext
Flask==2.1.1
gunicorn==20.1.0
```
### 1.4 app.yaml
Die Datei app.yaml dient zur Konfiguration für Google App Engine:

```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT app:app

#optional
handlers:
  - url: /static
    static_dir: static

  - url: /.*
    script: auto
```
Diese Konfiguration legt fest, dass deine Anwendung unter der Python 3.9-Laufzeitumgebung laufen wird und wie statische Dateien behandelt werden sollen. Außerdem wird so der entrypoint festgelegt.

## 2. Google Cloud einrichten

### 2.1 Anmeldung bei Google Cloud
Melde dich bei deinem Google Cloud Konto an und erstelle ein neues Projekt. Dieses Projekt wird verwendet, um deine Flask-Anwendung zu hosten.

### 2.2 Google Cloud SDK installieren
Wenn du das Google Cloud SDK noch nicht installiert hast, lade es herunter und installiere es gemäß der Anleitung auf Google Cloud SDK Installationsseite.

### 2.3 Einrichtung eines Zahlungskontos
Obwohl Google Cloud einen kostenlosen Testzeitraum bietet, musst du dennoch ein Zahlungskonto hinterlegen. Dies dient als Sicherheit für den Fall, dass deine Nutzung den kostenlosen Rahmen überschreitet.

### 2.4 Zugriffsberechtigungen einstellen
Stelle sicher, dass du die richtigen Zugriffsberechtigungen hast, um Projekte zu erstellen und zu verwalten. Dies kannst du unter "IAM & Verwaltung" in der Google Cloud Console überprüfen.

## 3. Deployment der Flask-Anwendung

### 3.1 Authentifizierung
Authentifiziere dich mit deinem Google Cloud Konto:

```bash
gcloud auth login
```
### 3.2 Projekt auswählen
Wähle das Projekt aus, in dem die Anwendung bereitgestellt werden soll:

```bash
gcloud config set project [DEIN-PROJEKT-ID]
```
### 3.3 App Engine initialisieren
Initialisiere die App Engine in deinem Projekt:

```bash
gcloud app create --region=[DEINE-REGION]
```
Wähle eine Region aus, die deinen Nutzern geografisch nahe liegt, um die Latenzzeiten zu minimieren.

### 3.4 Deployment
Um deine Anwendung auf Google App Engine zu deployen, führe folgenden Befehl aus:

```bash
gcloud app deploy
```
Dieser Befehl nimmt die app.yaml Datei und stellt die Anwendung auf der App Engine bereit. Der Deploymentsprozess kann einige Minuten dauern.

### 3.5 Anwendung anzeigen
Nachdem das Deployment erfolgreich abgeschlossen ist, kannst du deine Anwendung im Browser anzeigen lassen:

```bash
gcloud app browse
```
Dieser Befehl öffnet die URL deiner bereitgestellten Anwendung im Standardbrowser.

### 3.6 Zugriff auf Log-Informationen

Wenn während des Betriebs deiner Anwendung unerwartete Probleme auftreten, kannst du detaillierte Log-Informationen abrufen, um die Ursache zu identifizieren:

```bash
gcloud app logs tail -s default
```

## 4. Backend über LocalTunnel laufen lassen

Wenn du das Backend lokal testweise betreiben möchtest, kannst du LocalTunnel verwenden, um es für das Internet zugänglich zu machen.

### 4.1 Was ist LocalTunnel?
LocalTunnel ist ein einfaches Tool, das es dir ermöglicht, einen lokalen Server für das Internet zugänglich zu machen. Es erstellt einen sicheren Tunnel von deinem lokalen Rechner zu einer öffentlich zugänglichen URL, die du dann verwenden kannst, um deine Anwendung extern zu testen, ohne sie vollständig zu deployen. Dies ist besonders nützlich für das Testen von Webhooks, APIs oder das Teilen deiner lokalen Anwendung mit anderen, ohne dass eine vollständige Produktionsumgebung erforderlich ist.

### 4.2 Installation von LocalTunnel
Installiere [LocalTunnel](https://pypi.org/project/py-localtunnel/):

```bash
pip3 install py-localtunnel
```
### 4.3 Starten von LocalTunnel
Starte LocalTunnel und leite den Port deiner Flask-Anwendung weiter:

```bash
plt --port 5000
```
LocalTunnel generiert eine öffentliche URL, die auf deinen lokalen Server verweist. Diese kannst du dann verwenden, um das Backend zu testen.