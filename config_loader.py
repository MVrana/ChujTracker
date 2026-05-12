import configparser
import os
import sys

CONFIG_FILE = 'config.cfg'
EXAMPLE_CONFIG_FILE = 'config.example.cfg'

def load_config():
    """Načte konfiguraci z .cfg souboru"""
    config = configparser.ConfigParser()
    
    # Pokud config.cfg neexistuje, zkusit config.example.cfg
    if not os.path.exists(CONFIG_FILE):
        if os.path.exists(EXAMPLE_CONFIG_FILE):
            print(f"⚠️  Soubor {CONFIG_FILE} nenalezen. Zkopíruj {EXAMPLE_CONFIG_FILE} na {CONFIG_FILE}")
            print(f"   Copy-Item {EXAMPLE_CONFIG_FILE} {CONFIG_FILE}")
            sys.exit(1)
        else:
            print(f"❌ Soubory {CONFIG_FILE} ani {EXAMPLE_CONFIG_FILE} neexistují!")
            sys.exit(1)
    
    try:
        config.read(CONFIG_FILE, encoding='utf-8')
        return config
    except Exception as e:
        print(f"❌ Chyba při čtení konfigurace: {e}")
        sys.exit(1)

def get_database_config(config):
    """Vrátí konfiguraci databáze"""
    try:
        db_config = {
            'host': config.get('database', 'host', fallback='localhost'),
            'port': config.getint('database', 'port', fallback=3306),
            'user': config.get('database', 'user', fallback='root'),
            'password': config.get('database', 'password', fallback=''),
            'database': config.get('database', 'database', fallback='chujtracker'),
        }
        return db_config
    except Exception as e:
        print(f"❌ Chyba při načítání konfigurace databáze: {e}")
        sys.exit(1)

def get_flask_config(config):
    """Vrátí konfiguraci Flask"""
    try:
        flask_config = {
            'debug': config.getboolean('flask', 'debug', fallback=False),
            'host': config.get('flask', 'host', fallback='127.0.0.1'),
            'port': config.getint('flask', 'port', fallback=5000),
        }
        return flask_config
    except Exception as e:
        print(f"❌ Chyba při načítání Flask konfigurace: {e}")
        sys.exit(1)

def get_auth_config(config):
    """Vrátí konfiguraci autentifikace"""
    try:
        auth_config = {
            'password': config.get('auth', 'password', fallback='admin'),
        }
        return auth_config
    except Exception as e:
        print(f"❌ Chyba při načítání autentifikační konfigurace: {e}")
        sys.exit(1)

def create_example_config():
    """Vytvoří příklad config souboru, pokud neexistuje"""
    if not os.path.exists(EXAMPLE_CONFIG_FILE):
        example_content = """[database]
# MySQL databáze připojení
host = localhost
port = 3306
user = root
password = 
database = chujtracker

[flask]
# Flask nastavení
debug = true
host = 127.0.0.1
port = 5000

[auth]
# Jednoduchá autentifikace
password = admin123
"""
        try:
            with open(EXAMPLE_CONFIG_FILE, 'w', encoding='utf-8') as f:
                f.write(example_content)
            print(f"✓ Vytvořen příklad konfigurace: {EXAMPLE_CONFIG_FILE}")
        except Exception as e:
            print(f"❌ Chyba při vytváření příkladu konfigurace: {e}")
