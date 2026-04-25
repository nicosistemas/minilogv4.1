import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_DIR = os.path.join(DATA_DIR, "users")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CTY_FILE = os.path.join(BASE_DIR, "cty.dat")

SECRET_KEY = os.environ.get("SECRET_KEY", "changeme-in-production")

STORAGE_BACKEND = os.environ.get("STORAGE_BACKEND", "csv")  # csv | sqlite (futuro)

MODES = ["SSB", "CW", "FT8", "FM", "AM", "DIGITALV", "OTHER"]

CONTACTS_HEADER = ["date", "callsign", "mode", "frequency", "notes", "operator"]
