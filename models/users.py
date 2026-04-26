import json
import os
import secrets
from datetime import datetime, timedelta, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from config import USERS_FILE, USERS_DIR, RESET_TOKENS_FILE, RESET_TOKEN_EXPIRY_MINUTES


def _load_db() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_db(db: dict) -> None:
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def _load_tokens() -> dict:
    if not os.path.exists(RESET_TOKENS_FILE):
        return {}
    with open(RESET_TOKENS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_tokens(tokens: dict) -> None:
    os.makedirs(os.path.dirname(RESET_TOKENS_FILE), exist_ok=True)
    with open(RESET_TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2)


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
    def list_all() -> list:
        db = _load_db()
        result = []
        for callsign in db:
            user_dir = os.path.join(USERS_DIR, callsign)
            contacts_file = os.path.join(user_dir, "contacts.csv")
            contact_count = 0
            if os.path.exists(contacts_file):
                with open(contacts_file, encoding="utf-8") as f:
                    contact_count = sum(1 for line in f if line.strip())
            result.append({"callsign": callsign, "contacts": contact_count})
        return sorted(result, key=lambda x: x["callsign"])

    @staticmethod
    def register(callsign: str, password: str) -> "User | None":
        db = _load_db()
        key = callsign.upper()
        if key in db:
            return None
        db[key] = generate_password_hash(password)
        _save_db(db)
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

    @staticmethod
    def set_password(callsign: str, new_password: str) -> bool:
        db = _load_db()
        key = callsign.upper()
        if key not in db:
            return False
        db[key] = generate_password_hash(new_password)
        _save_db(db)
        return True

    @staticmethod
    def delete(callsign: str) -> bool:
        db = _load_db()
        key = callsign.upper()
        if key not in db:
            return False
        del db[key]
        _save_db(db)
        return True

    @staticmethod
    def generate_reset_token(callsign: str) -> "str | None":
        db = _load_db()
        key = callsign.upper()
        if key not in db:
            return None
        token = secrets.token_urlsafe(32)
        expiry = (datetime.now(timezone.utc) +
                  timedelta(minutes=RESET_TOKEN_EXPIRY_MINUTES)).isoformat()
        tokens = _load_tokens()
        tokens = {t: v for t, v in tokens.items() if v["callsign"] != key}
        tokens[token] = {"callsign": key, "expiry": expiry}
        _save_tokens(tokens)
        return token

    @staticmethod
    def validate_reset_token(token: str) -> "str | None":
        tokens = _load_tokens()
        if token not in tokens:
            return None
        entry = tokens[token]
        expiry = datetime.fromisoformat(entry["expiry"])
        if datetime.now(timezone.utc) > expiry:
            del tokens[token]
            _save_tokens(tokens)
            return None
        return entry["callsign"]

    @staticmethod
    def consume_reset_token(token: str, new_password: str) -> bool:
        callsign = User.validate_reset_token(token)
        if not callsign:
            return False
        User.set_password(callsign, new_password)
        tokens = _load_tokens()
        tokens.pop(token, None)
        _save_tokens(tokens)
        return True
