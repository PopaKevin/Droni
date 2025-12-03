from flask import current_app, g
# Importa il driver del database che userai, ad esempio per MySQL:
# import mysql.connector 
# oppure un driver come PyMySQL
import sys

# Utilizziamo un driver generico per il placeholder
# Si dovrà installare il driver specifico (es. 'pip install PyMySQL')

class DBConnectionError(Exception):
    """Eccezione personalizzata per errori di connessione al DB."""
    pass

def get_db():
    """
    Stabilisce una connessione al database se non ne esiste già una nel contesto dell'applicazione.
    La connessione è memorizzata nell'oggetto `g` (global) di Flask.
    """
    if 'db_conn' not in g:
        # Qui si implementa la logica di connessione specifica per il driver scelto (es. PyMySQL, psycopg2)
        try:
            # Per ora, usiamo un placeholder concettuale.
            # Esempio concettuale (SOSTITUIRE CON LA LOGICA REALE):
            
            # if current_app.config['DB_DRIVER'] == 'mysql':
            #     import mysql.connector
            #     g.db_conn = mysql.connector.connect(
            #         host=current_app.config['DB_HOST'],
            #         user=current_app.config['DB_USER'],
            #         password=current_app.config['DB_PASSWORD'],
            #         database=current_app.config['DB_NAME']
            #     )
            # else:
            #     raise NotImplementedError("Driver DB non supportato")
            
            # Placeholder: Simula un oggetto connessione
            print("Tentativo di connessione al database...")
            g.db_conn = "DB_CONNESSO_PLACEHOLDER" 
            print("Connessione DB riuscita (simulata).")
            
        except Exception as e:
            print(f"ERRORE DI CONNESSIONE DB: {e}", file=sys.stderr)
            raise DBConnectionError(f"Impossibile connettersi al database: {e}")

    return g.db_conn

def close_db(e=None):
    """
    Chiude la connessione al database se è stata stabilita.
    Chiamata automaticamente alla fine di ogni richiesta.
    """
    db_conn = g.pop('db_conn', None)

    if db_conn is not None and db_conn != "DB_CONNESSO_PLACEHOLDER":
        # Chiude la connessione reale
        # db_conn.close() 
        pass
    elif db_conn == "DB_CONNESSO_PLACEHOLDER":
         print("Chiusura connessione DB (simulata).")

def init_app(app):
    """Registra la funzione close_db per essere chiamata al teardown della richiesta."""
    app.teardown_appcontext(close_db)

# --- Funzioni di Interazione con il DB (Da Implementare in api.py o qui) ---

def fetch_order_status(order_id):
    """Recupera lo stato attuale di un ordine e i dati del drone in missione."""
    db = get_db()
    # Esegui query SQL e ritorna il risultato
    # Esempio: SELECT stato, drone_id FROM Ordine WHERE id = %s
    # Esempio: SELECT lat, lon FROM Traccia WHERE mission_id = (SELECT mission_id FROM Ordine...) ORDER BY timestamp DESC LIMIT 1
    
    print(f"Query DB: Recupero stato ordine {order_id} e posizione drone...")
    # Dati fittizi per testing Frontend
    return {
        "status": "in_consegna",
        "current_position": {"lat": 45.4642, "lon": 9.1900}, # Posizione a Milano (Placehold)
        "drone_id": "DRN-001",
        "last_update": "2025-12-03T11:00:00Z"
    }

# Altre funzioni CRUD/Analisi (es. gestisci_drone, recupera_missioni_pilota, ecc.) andranno qui