from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import login_required, current_user

from models.contacts import (
    append_contact, delete_contact, load_contacts, update_contact
)
from config import MODES

main_bp = Blueprint("main", __name__)


def _parse_frequency(raw: str) -> str | None:
    try:
        freq = float(raw.replace(",", "."))
        return f"{freq:.3f}"
    except ValueError:
        return None


@main_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        callsign  = request.form.get("callsign", "").strip().upper()
        mode      = request.form.get("mode", "")
        freq_raw  = request.form.get("frequency", "")
        notes     = request.form.get("notes", "")

        frequency = _parse_frequency(freq_raw)
        if not frequency or not callsign:
            return redirect(url_for("main.index"))

        append_contact(current_user.id, callsign, mode, frequency, notes)

        # Guardar last_mode y last_frequency en sesión
        session["last_mode"]      = mode
        session["last_frequency"] = frequency

        return redirect(url_for("main.index"))

    contacts = load_contacts(current_user.id)
    contacts_with_index = list(enumerate(contacts))[::-1]

    return render_template(
        "index.html",
        contacts=contacts_with_index,
        last_mode=session.get("last_mode", ""),
        last_frequency=session.get("last_frequency", ""),
        modes=MODES,
    )


@main_bp.route("/edit/<int:index>", methods=["GET", "POST"])
@login_required
def edit(index):
    contacts = load_contacts(current_user.id)

    if index >= len(contacts):
        return "Contacto no encontrado", 404

    if request.method == "POST":
        callsign = request.form.get("callsign", "").strip().upper()
        mode     = request.form.get("mode", "")
        freq_raw = request.form.get("frequency", "")
        notes    = request.form.get("notes", "")

        frequency = _parse_frequency(freq_raw)
        if not frequency or not callsign:
            return redirect(url_for("main.index"))

        update_contact(current_user.id, index, callsign, mode, frequency, notes)
        return redirect(url_for("main.index"))

    return render_template("edit.html", contact=contacts[index], index=index, modes=MODES)


@main_bp.route("/delete/<int:index>")
@login_required
def delete(index):
    try:
        delete_contact(current_user.id, index)
    except IndexError:
        return "Contacto no encontrado", 404
    return redirect(url_for("main.index"))
