import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables desde .env

class Config:
    # Si no hay DATABASE_URL en .env, usa SQLite local
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///presenciauba.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")  # Clave secreta para sesiones
