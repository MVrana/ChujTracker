from flask import Flask, render_template, request, jsonify
from config_loader import load_config, get_flask_config
from database import (
    init_db, get_all_people, add_person, get_person,
    update_points, delete_person, person_exists
)

# Načti Flask konfiguraci
config = load_config()
flask_config = get_flask_config(config)

app = Flask(__name__, static_folder='static', template_folder='templates')

# Inicializace databáze
init_db()

@app.route('/')
def index():
    """Hlavní stránka"""
    return render_template('index.html')

@app.route('/api/people', methods=['GET'])
def get_people():
    """Vrátí seznam všech lidí"""
    people = get_all_people()
    return jsonify(people)

@app.route('/api/people', methods=['POST'])
def add_person_route():
    """Přidá nového člověka"""
    person_name = request.json.get('name', '').strip()
    
    if not person_name:
        return jsonify({'error': 'Jméno je povinné'}), 400
    
    # Zkontroluj, zda člověk již neexistuje
    if person_exists(person_name):
        return jsonify({'error': 'Tento člověk již existuje'}), 400
    
    try:
        new_person = add_person(person_name)
        return jsonify(new_person), 201
    except Exception as e:
        return jsonify({'error': 'Chyba při přidávání člověka'}), 400

@app.route('/api/people/<int:person_id>/points', methods=['POST'])
def update_person_points(person_id):
    """Aktualizuje body pro konkrétního člověka"""
    person = get_person(person_id)
    if not person:
        return jsonify({'error': 'Člověk nenalezen'}), 404
    
    change = request.json.get('change', 0)
    updated_person = update_points(person_id, change)
    return jsonify(updated_person)

@app.route('/api/people/<int:person_id>', methods=['DELETE'])
def delete_person_route(person_id):
    """Smaže člověka"""
    success = delete_person(person_id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Člověk nenalezen'}), 404

if __name__ == '__main__':
    app.run(
        debug=flask_config['debug'],
        host=flask_config['host'],
        port=flask_config['port']
    )
