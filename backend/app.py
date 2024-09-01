from flask import Flask, jsonify, request
from datetime import datetime
from create import initialize_inventory
from flask_httpauth import HTTPBasicAuth
import sqlite3


app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": "secret",
    "user": "password"
}

# Authentifizierung 
@auth.verify_password
def verify_password(username, password):
    if users.get(username) == password:
        return username
    
# Verbindung zur SQLite-Datenbank
def get_db_connection():
    conn = sqlite3.connect('bestellungen.db')
    conn.row_factory = sqlite3.Row
    return conn

# Endpunkt zum Abrufen von Produkten mit deren Lagerbeständen
@app.route('/api/products', methods=['GET'])
@auth.login_required
def api_get_products():
    try:
        conn = get_db_connection()
        products = conn.execute('''
        SELECT p.ProduktId, p.Name, l.VerfuegbareMenge
        FROM Produkte p
        JOIN Lagerbestand l ON p.ProduktId = l.ProduktId
        ''').fetchall()
        conn.close() 
        return jsonify([dict(product) for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpunkt zur Bestllungsaufgabe 
@app.route('/api/order', methods=['POST'])
@auth.login_required
def api_place_order():
    data = request.get_json()
    if not data or 'orders' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    orders = data['orders']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insufficient_stock = [] # Liste für Produkte mit unzureichendem Lagerbestand
        for order in orders:
            produkt_id = order['ProduktId']
            menge = order['Menge']
            cursor.execute('SELECT VerfuegbareMenge FROM Lagerbestand WHERE ProduktId = ?', (produkt_id,))
            available_stock = cursor.fetchone()[0]
            if available_stock < menge:
                insufficient_stock.append(produkt_id)

        if insufficient_stock: 
            return jsonify({'error': 'Some products are out of stock or insufficient in quantity.', 'products': insufficient_stock}), 400

        cursor.execute('INSERT INTO Bestellungen (Bestelldatum) VALUES (?)', (datetime.now(),))
        bestell_id = cursor.lastrowid
        for order in orders:
            produkt_id = order['ProduktId']
            menge = order['Menge']
            cursor.execute('INSERT INTO Bestellungsprodukte (BestellId, ProduktId, Menge) VALUES (?, ?, ?)', (bestell_id, produkt_id, menge))
            cursor.execute('UPDATE Lagerbestand SET VerfuegbareMenge = VerfuegbareMenge - ? WHERE ProduktId = ?', (menge, produkt_id))
        
        conn.commit()
        return jsonify({'message': 'Order placed successfully!'}), 201
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# Endpunkt für den Reset der Lagerbestände
@app.route('/api/reset', methods=['POST'])
@auth.login_required
def api_reset_inventory():
    try:
        initialize_inventory('bestellungen.db')
        return jsonify({'message': 'Inventory reset successfully!'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run()