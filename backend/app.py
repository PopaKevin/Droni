from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config
from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)                 # abilita richieste cross-origin (frontend separato)
db = SQLAlchemy(app)      # inizializza SQLAlchemy
app.secret_key = Config.SECRET_KEY

@app.route("/missioni")
def missioni():
    try:
        result = db.session.execute(text("SELECT * FROM Missioni LIMIT 5;"))
        rows = []
        for row in result.mappings():
            row_dict = dict(row)
            # Converte tutti i datetime e timedelta in stringhe
            for key, value in row_dict.items():
                if isinstance(value, (datetime.datetime, datetime.date, datetime.time, datetime.timedelta)):
                    row_dict[key] = str(value)
            rows.append(row_dict)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"errore": str(e)})

@app.route("/test-db")
def test_db():
    try:
        db.session.execute(text("SELECT 1;"))
        return "Connessione al database Aiven OK! 🚀"
    except Exception as e:
        return f"❌ Errore connessione DB: {str(e)}"

@app.route("/ordini/<int:id>")
def get_ordine(id):
    try:
        result = db.session.execute(text("SELECT * FROM Ordine WHERE ID = :id"), {"id": id})
        ordine = result.mappings().first()
        if not ordine:
            return jsonify({"errore": "Ordine non trovato"}), 404
        ordine_dict = dict(ordine)
        # eventuale conversione datetime
        for k, v in ordine_dict.items():
            if isinstance(v, (datetime.datetime, datetime.date, datetime.time, datetime.timedelta)):
                ordine_dict[k] = str(v)
        # Recupero prodotti contenuti nell'ordine
        prodotti_result = db.session.execute(text("""
            SELECT P.nome, P.peso, P.categoria, C.Quantita
            FROM Contiene C
            JOIN Prodotto P ON C.ID_Prodotto = P.ID
            WHERE C.ID_Ordine = :id
        """), {"id": id})
        ordine_dict["prodotti"] = [dict(r) for r in prodotti_result.mappings()]
        return jsonify(ordine_dict)
    except Exception as e:
        return jsonify({"errore": str(e)})

@app.route("/missioni/<int:id>/tracce")
def tracce_missione(id):
    try:
        result = db.session.execute(text("""
            SELECT Latitudine, Longitudine, TIMESTAMP
            FROM Traccia
            WHERE ID_Missione = :id
            ORDER BY TIMESTAMP ASC
        """), {"id": id})
        rows = []
        for row in result.mappings():
            row_dict = dict(row)
            # Converti datetime in stringa
            if "TIMESTAMP" in row_dict:
                row_dict["TIMESTAMP"] = str(row_dict["TIMESTAMP"])
            rows.append(row_dict)
        return jsonify(rows)
    except Exception as e:
        return jsonify({"errore": str(e)})

from flask import request

@app.route("/valutazioni", methods=["POST"])
def inserisci_valutazione():
    try:
        data = request.get_json()
        db.session.execute(text("""
            UPDATE Missione
            SET Valutazione = :val
            WHERE ID = :id
        """), {"val": data["valutazione"], "id": data["id_missione"]})
        db.session.commit()
        return jsonify({"successo": True})
    except Exception as e:
        return jsonify({"errore": str(e)})

@app.route("/droni")
def get_droni():
    result = db.session.execute(text("SELECT * FROM Drone"))
    return jsonify([dict(r) for r in result.mappings()])

@app.route("/piloti")
def get_piloti():
    result = db.session.execute(text("SELECT * FROM Pilota"))
    return jsonify([dict(r) for r in result.mappings()])

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"errore": "Email e password obbligatorie"}), 400

    # Controllo nel DB
    try:
        user = db.session.execute(
            text("SELECT * FROM Utente WHERE Mail=:email AND Password=:pwd"),
            {"email": email, "pwd": password}
        ).mappings().first()

        if user:
            session["user_id"] = user["ID"]
            session["ruolo"] = user["Ruolo"]

            return jsonify({"successo": True, "ruolo": user["Ruolo"]})
        else:
            return jsonify({"errore": "Email o password errate"}), 401
    except Exception as e:
        return jsonify({"errore": str(e)}), 500



if __name__ == "__main__":
    import datetime
    app.run(debug=True, port=5002)
