from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config  # importa il tuo config.py

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Modello di test semplice
class TestConn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))

if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()  # prova a creare la tabella
        print("✅ Connessione funzionante! Tabella creata correttamente.")
    except Exception as e:
        print("❌ Errore di connessione:", e)
