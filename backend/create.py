import sqlite3

def create_tables(db_file):
    try:

        # Verbindung zur SQLite-Datenbank herstellen
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()  

        # Tabelle "Produkte" erstellen
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produkte (
            ProduktId INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Haltbarkeit DATE,
            Zerbrechlichkeitslevel INTEGER,
            UNIQUE(Name)
        )
        ''')

        # Tabelle "Bestellungen" erstellen
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bestellungen (
            BestellId INTEGER PRIMARY KEY AUTOINCREMENT,
            Bestelldatum DATETIME NOT NULL
        )
        ''')

        # Tabelle "Bestellungsprodukte" erstellen
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bestellungsprodukte (
            BestellId INTEGER,
            ProduktId INTEGER,
            Menge INTEGER NOT NULL,
            PRIMARY KEY (BestellId, ProduktId),
            FOREIGN KEY (BestellId) REFERENCES Bestellungen(BestellId),
            FOREIGN KEY (ProduktId) REFERENCES Produkte(ProduktId)
        )
        ''')

          # Tabelle "Lagerbestand" erstellen
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Lagerbestand (
            ProduktId INTEGER PRIMARY KEY,
            VerfuegbareMenge INTEGER NOT NULL,
            FOREIGN KEY (ProduktId) REFERENCES Produkte(ProduktId)
        )
        ''')

        # Änderungen speichern und Verbindung schließen
        conn.commit()
        print("Tabellen erfolgreich erstellt.")
        
    except sqlite3.Error as e:
        print(f"Fehler beim Erstellen der Tabellen: {e}")
    finally:
        if conn:
            conn.close()

def initialize_inventory(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Clear the current inventory and products
        cursor.execute('DELETE FROM Lagerbestand')

        # Fiktive Produkte einfügen
        products = [
            ("Tomaten", "2024-08-15", 2),
            ("Apfel", "2024-09-01", 1),
            ("Eier", "2024-08-07", 3),
            ("Bananen", "2024-08-10", 2),
            ("Kidneybohnen", "2025-02-01", 0),
            ("Spaghetti", "2025-06-01", 0),
            ("Chips", "2024-12-01", 2),
            ("Eis", "2024-08-01", 1),
            ("Mozzarella", "2024-08-05", 1)
        ]
        cursor.executemany('INSERT OR IGNORE INTO Produkte (Name, Haltbarkeit, Zerbrechlichkeitslevel) VALUES (?, ?, ?)', products)

        # Fiktive Lagerbestände hinzufügen
        inventory = [
            (1, 10),  # Tomaten
            (2, 10),  # Apfel
            (3, 30),  # Eier
            (4, 50),  # Bananen
            (5, 50),  # Kidneybohnen
            (6, 25),  # Spaghetti
            (7, 15),  # Chips
            (9, 20),   # Eis
            (10, 35)   # Mozzarella
        ]
        cursor.executemany('INSERT OR IGNORE INTO Lagerbestand (ProduktId, VerfuegbareMenge) VALUES (?, ?)', inventory)

        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Fehler beim Initialisieren des Lagerbestands: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    db_file = 'backend/bestellungen.db'
    create_tables(db_file)
    initialize_inventory(db_file)