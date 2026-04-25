from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from models.contacts import append_contact, load_contacts
from storage import storage

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/qso", methods=["POST"])
@login_required
def api_qso():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "no data"}), 400

    callsign  = data.get("call", "").strip().upper()
    mode      = data.get("mode", "")
    freq      = str(data.get("freq", ""))
    notes     = data.get("extra", "")
    timestamp = data.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not callsign:
        return jsonify({"error": "missing call"}), 400

    # Insertar directamente con timestamp externo
    contact = [timestamp, callsign, mode, freq, notes, current_user.id]
    storage.append_contact(current_user.id, contact)

    return jsonify({"status": "ok", "call": callsign, "mode": mode}), 201


@api_bp.route("/qso", methods=["GET"])
@login_required
def api_list():
    contacts = load_contacts(current_user.id)
    result = [
        {
            "date":      c[0],
            "callsign":  c[1],
            "mode":      c[2],
            "frequency": c[3],
            "notes":     c[4] if len(c) > 4 else "",
            "operator":  c[5] if len(c) > 5 else "",
        }
        for c in contacts
    ]
    return jsonify(result)
