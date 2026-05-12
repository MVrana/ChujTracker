# ChujTracker

Jednoduchá webová aplikace pro sledování bodů praktikantů během praxe. Umožňuje přidávat, mazat a aktualizovat body jednotlivých osob. Zobrazení osob a jejich bodů je veřejné, ale administrativní akce vyžadují jednoduché přihlášení pomocí hesla.

## Funkce

- **Přidávání osob**: Přidej nové praktikanty do systému
- **Sledování bodů**: Zobraz aktuální počet bodů pro každého člověka
- **Aktualizace bodů**: Zvyšuj nebo snižuj body podle výkonu
- **Mazání osob**: Odstraň praktikanty ze systému
- **Webové rozhraní**: Jednoduché a intuitivní UI
- **Autentifikace**: Pro administrativní akce (přidání, úprava, mazání) je vyžadováno heslo

## Technologie

- **Backend**: Flask (Python)
- **Databáze**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **API**: RESTful API pro komunikaci s databází

## Instalace a spuštění

1. **Naklonuj repozitář**:
   ```bash
   git clone https://github.com/MVrana/ChujTracker.git
   cd ChujTracker
   ```

2. **Nainstaluj závislosti**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Nastav databázi**:
   - Uprav `config.cfg` podle svého MySQL připojení
   - Aplikace automaticky vytvoří potřebné tabulky při prvním spuštění
   - V sekci `[auth]` nastav heslo pro administraci
   - Výchozí heslo je `admin123`, pokud není v `config.cfg` uvedeno jiné

4. **Spusť aplikaci**:
   ```bash
   python app.py
   ```

5. **Otevři v prohlížeči**:
   - Přejdi na `http://127.0.0.1:5000`

## API Endpoints

- `GET /api/people` - Získání seznamu všech osob
- `POST /api/people` - Přidání nové osoby (vyžaduje heslo)
- `POST /api/people/<id>/points` - Aktualizace bodů (vyžaduje heslo)
- `DELETE /api/people/<id>` - Smazání osoby (vyžaduje heslo)

## Struktura projektu

```
ChujTracker/
├── app.py              # Hlavní Flask aplikace
├── config_loader.py    # Načítání konfigurace
├── database.py         # Databázové operace
├── config.cfg          # Konfigurační soubor
├── requirements.txt    # Python závislosti
├── static/             # CSS a JS soubory
├── templates/          # HTML šablony
└── README.md           # Tento soubor
```

## Poznámky

- Aplikace používá free MySQL databázi (freesqldatabase.com)
- Pro produkční nasazení doporučuji použít vlastní databázový server
- Debug mód je ve výchozím nastavení zapnutý