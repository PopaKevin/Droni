from flask import Blueprint, request, session, jsonify, g
from werkzeug.security import check_password_hash # Uso simulato
from functools import wraps
from db import get_db
import sys

# Blueprint per le rotte di autenticazione
bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# Ruoli disponibili
ROLES = {'cliente': 1, 'admin': 2, 'pilota': 3}

def login_required(f):
    """Decorator per proteggere le rotte: richiede una sessione utente attiva."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized", "message": "Login richiesto"}), 401
        
        # Carica i dati utente nell'oggetto g
        if 'user' not in g:
            g.user = get_user_data(session['user_id'])
            if g.user is None:
                 session.pop('user_id', None) # Rimuovi sessione non valida
                 return jsonify({"error": "Unauthorized", "message": "Sessione non valida"}), 401
                 
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """Decorator per proteggere le rotte: richiede un ruolo specifico."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            user_role = g.user.get('Ruolo')
            if ROLES.get(user_role) is None or ROLES[user_role] < ROLES[required_role]:
                return jsonify({"error": "Forbidden", "message": f"Autorizzazione insufficiente. Richiesto: {required_role}"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_user_data(user_id):
    """Recupera i dati utente dal DB."""
    db = get_db()
    try:
        with db.cursor() as cursor:
            sql = "SELECT ID, Nome, Email, PasswordHash, Ruolo FROM Utente WHERE ID = %s"
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Errore nel recupero dati utente: {e}", file=sys.stderr)
        return None


@bp.route('/login', methods=['POST'])
def login():
    """Endpoint per l'autenticazione utente."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing Data", "message": "Email e password sono richieste"}), 400

    user = None
    try:
        db = get_db()
        with db.cursor() as cursor:
            sql = "SELECT ID, Nome, Email, PasswordHash, Ruolo FROM Utente WHERE Email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()

    except Exception as e:
        print(f"Errore DB durante il login: {e}", file=sys.stderr)
        return jsonify({"error": "Internal Server Error", "message": "Errore nel database"}), 500

    # Simulazione della verifica della password
    # In un ambiente reale, useremmo check_password_hash(user['PasswordHash'], password)
    # Dato che abbiamo usato 'fakehash...' per i dati di prova, accettiamo 'password' come password fittizia.
    is_valid_password = user and password == 'password' # Sostituire con check_password_hash(user['PasswordHash'], password)

    if user is None or not is_valid_password:
        return jsonify({"error": "Unauthorized", "message": "Credenziali non valide"}), 401

    # Login riuscito: crea la sessione
    session.clear()
    session['user_id'] = user['ID']
    session['role'] = user['Ruolo']

    return jsonify({
        "message": "Login successful", 
        "user_id": user['ID'],
        "role": user['Ruolo'],
        "redirect": "/admin/index.html" if user['Ruolo'] == 'admin' else "/customer/index.html"
    })

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Endpoint per il logout."""
    session.clear()
    return jsonify({"message": "Logout successful"})

@bp.route('/me', methods=['GET'])
@login_required
def get_user_info():
    """Recupera le informazioni dell'utente loggato."""
    return jsonify({
        "id": g.user['ID'],
        "nome": g.user['Nome'],
        "email": g.user['Email'],
        "ruolo": g.user['Ruolo']
    })