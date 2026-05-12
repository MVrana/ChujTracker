import mysql.connector
from mysql.connector import Error
from config_loader import load_config, get_database_config

class DatabaseConnection:
    """Spravuje připojení k MySQL databázi"""
    
    def __init__(self, config=None):
        if config is None:
            cfg = load_config()
            config = get_database_config(cfg)
        self.config = config
        self.connection = None
    
    def connect(self):
        """Vytvoří připojení k databázi"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
            if self.connection.is_connected():
                print(f"✓ Připojeno k databázi: {self.config['database']} na {self.config['host']}:{self.config['port']}")
                self._init_tables()
                return True
        except Error as e:
            print(f"✗ Chyba připojení k databázi: {e}")
            return False
    
    def disconnect(self):
        """Ukončí připojení k databázi"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Připojení k databázi ukončeno")
    
    def get_connection(self):
        """Vrátí aktivní připojení"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def _init_tables(self):
        """Vytvoří potřebné tabulky"""
        cursor = self.connection.cursor()
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS people (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            points INT DEFAULT 0,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        try:
            cursor.execute(create_table_sql)
            self.connection.commit()
            print("✓ Databázové tabulky připraveny")
        except Error as e:
            print(f"✗ Chyba při vytváření tabulek: {e}")
        finally:
            cursor.close()

# Globální instance připojení
_db_instance = None

def get_db():
    """Vrátí instanci databázového připojení"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection()
        _db_instance.connect()
    return _db_instance

def init_db():
    """Inicializuje databázi"""
    db = get_db()
    db.connect()

def get_all_people():
    """Vrátí seznam všech lidí"""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT id, name, points, created FROM people ORDER BY points DESC')
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Chyba při načítání lidí: {e}")
        return []
    finally:
        cursor.close()

def person_exists(name):
    """Zkontroluje, zda člověk již existuje"""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id FROM people WHERE LOWER(name) = LOWER(%s)', (name,))
        return cursor.fetchone() is not None
    except Error as e:
        print(f"Chyba při kontrole člověka: {e}")
        return False
    finally:
        cursor.close()

def add_person(name):
    """Přidá nového člověka"""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            'INSERT INTO people (name, points) VALUES (%s, 0)',
            (name.strip(),)
        )
        conn.commit()
        person_id = cursor.lastrowid
        
        cursor.execute('SELECT id, name, points, created FROM people WHERE id = %s', (person_id,))
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Chyba při přidávání člověka: {e}")
        raise
    finally:
        cursor.close()

def get_person(person_id):
    """Vrátí konkrétního člověka"""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute('SELECT id, name, points, created FROM people WHERE id = %s', (person_id,))
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Chyba při načítání člověka: {e}")
        return None
    finally:
        cursor.close()

def update_points(person_id, change):
    """Aktualizuje body pro konkrétního člověka"""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute('UPDATE people SET points = points + %s WHERE id = %s', (change, person_id))
        conn.commit()
        
        cursor.execute('SELECT id, name, points, created FROM people WHERE id = %s', (person_id,))
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Chyba při aktualizaci bodů: {e}")
        return None
    finally:
        cursor.close()

def delete_person(person_id):
    """Smaže člověka"""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM people WHERE id = %s', (person_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Chyba při mazání člověka: {e}")
        return False
    finally:
        cursor.close()

def reset_all_points():
    """Resetuje všechny body na 0"""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE people SET points = 0')
        conn.commit()
    except Error as e:
        print(f"Chyba při resetování bodů: {e}")
    finally:
        cursor.close()

def delete_all_people():
    """Smaže všechny lidi"""
    db = get_db()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM people')
        conn.commit()
    except Error as e:
        print(f"Chyba při mazání všech lidí: {e}")
    finally:
        cursor.close()
