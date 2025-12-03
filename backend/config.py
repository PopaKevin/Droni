import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SSL_CERT = os.getenv("DB_SSL_CERT")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersegreto-che-devi-cambiare")
    SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://avnadmin:AVNS_6cw3jnc0lxZj1HoeX9a"
    "@mysql-3fe90f59-iisgalvanimi-1c9f.e.aivencloud.com:12798/Droni"
    "?ssl_ca=certs/ca.pem"
)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
