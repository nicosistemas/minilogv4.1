from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from storage import storage
from models.contacts import load_contacts
from models.users import User

api_bp = Blueprint("api", __name__, url_prefix="/api")

API_TOKEN = "radioaficionado"


def _check_token() -> bool:
    """Valida el token en el header Authorization: Bearer <token>"""
    auth = request.headers.get("Authorization", "")
    return auth == f"Bearer {API_TOKEN}"


@api_bp.route("/status", methods=["GET"])
def api_status():
    """Estado de la API — público, sin autenticación."""
    return jsonify({
        "status": "ok",
        "version": "1.0",
        "time_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    })


@api_bp.route("/qso", methods=["POST"])
def api_qso():
    """
    Registrar un QSO via API.

    Header requerido:
        Authorization: Bearer radioaficionado

    Body JSON:
    {
        "call":      "K1ABC",
        "mycall":    "LU2FTI",
        "mode":      "FT8",
        "freq":      14.074,
        "extra":     "notas",
        "timestamp": "2026-04-25 14:00:00"
    }
    """
    if not _check_token():
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "no data"}), 400

    call      = data.get("call", "").strip().upper()
    mode      = data.get("mode", "")
    freq      = data.get("freq", 0)
    mycall    = data.get("mycall", "").strip().upper()
    timestamp = data.get("timestamp")

    if not call:
        return jsonify({"error": "missing call"}), 400

    if not mycall:
        return jsonify({"error": "missing mycall"}), 400

    if not User.get(mycall):
        return jsonify({"error": f"{mycall} not registered"}), 403

    if not timestamp:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    contact = [
        timestamp,
        call,
        mode,
        str(freq),
        data.get("extra", ""),
        mycall,
    ]
    storage.append_contact(mycall, contact)

    return jsonify({
        "status": "ok",
        "call":   call,
        "mode":   mode,
        "mycall": mycall,
    }), 201


@api_bp.route("/qso", methods=["GET"])
@login_required
def api_list():
    """Lista QSOs del usuario autenticado (requiere sesión web)."""
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
    return jsonify({"operator": current_user.id, "total": len(result), "qsos": result})
