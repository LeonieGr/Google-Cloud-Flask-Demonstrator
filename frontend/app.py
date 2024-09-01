from flask import Flask, render_template, request, jsonify
from requests.auth import HTTPBasicAuth
import requests
import os
import json

# Basisverzeichnis und Pfade für Templates und statische Dateien
base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, 'config.json')

app = Flask(__name__)

# Lade Konfiguration aus JSON-Datei
with open(config_path) as config_file:
    config = json.load(config_file)


BACKEND_URL = os.getenv('BACKEND_URL', 'https://chatty-windows-fetch.loca.lt') # Backend URL von localtunnel
BACKEND_USER = os.getenv('BACKEND_USER', 'admin')
BACKEND_PASS = os.getenv('BACKEND_PASS', 'secret')

# Force Flask to reload templates automatically and explain the loading process
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

@app.route('/')
def index():
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    template_dir = os.path.join(cwd, 'templates')
    print(f"Templates directory: {template_dir}")
    print(f"Files in templates: {os.listdir(template_dir)}")
    return render_template('index.html')


# Sendet request für Produkte an das Backend
@app.route('/api/products', methods=['GET'])
def frontend_api_get_products():
    try:
        response = requests.get(f'{BACKEND_URL}/api/products', auth=HTTPBasicAuth(BACKEND_USER, BACKEND_PASS))
        response.raise_for_status()  # HTTP-Fehler abfangen
        products = response.json()
        return jsonify(products), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error while fetching products: {e}")
        return jsonify({'error': 'Failed to fetch products from backend'}), 500

# Sendet request für die Bestellung an das Backend
@app.route('/api/order', methods=['POST'])
def frontend_api_place_order():
    try:
        response = requests.post(f'{BACKEND_URL}/api/order', json=request.get_json(), auth=HTTPBasicAuth(BACKEND_USER, BACKEND_PASS))
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error while placing order: {e}")
        return jsonify({'error': 'Failed to place order'}), 500

# Sendet request für einen Inventory Reset an das Backend
@app.route('/api/reset', methods=['POST'])
def frontend_api_reset_inventory():
    try:
        response = requests.post(f'{BACKEND_URL}/api/reset', auth=HTTPBasicAuth(BACKEND_USER, BACKEND_PASS))
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error while resetting inventory: {e}")
        return jsonify({'error': 'Failed to reset inventory'}), 500

if __name__ == '__main__':
    app.run(debug=True)