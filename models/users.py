import json
import os

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from config import USERS_FILE, USERS_DIR


def _load_db() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_db(db: dict) -> None:
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


class User(UserMixin):
    def __init__(self, callsign: str):
        self.id = callsign.upper()

    @staticmethod
    def get(callsign: str) -> "User | None":
        db = _load_db()
        if callsign.upper() in db:
            return User(callsign.upper())
        return None

    @staticmethod
    def register(callsign: str, password: str) -> "User | None":
        """
        Registra un nuevo operador. Retorna None si el callsign ya existe.
        Crea automáticamente el directorio data/users/<callsign>/
        """
        db = _load_db()
        key = callsign.upper()
        if key in db:
            return None
        db[key] = generate_password_hash(password)
        _save_db(db)
        # Pre-crear directorio del usuario
        user_dir = os.path.join(USERS_DIR, key)
        os.makedirs(user_dir, exist_ok=True)
        return User(key)

    @staticmethod
    def authenticate(callsign: str, password: str) -> "User | None":
        db = _load_db()
        key = callsign.upper()
        if key not in db:
            return None
        if check_password_hash(db[key], password):
            return User(key)
        return None
