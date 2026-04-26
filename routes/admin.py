from flask import Blueprint, redirect, render_template, request, url_for, flash, session
from models.users import User
from config import ADMIN_PASSWORD

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _admin_required():
    return session.get("admin_logged_in") is True


@admin_bp.route("/", methods=["GET", "POST"])
def login():
    if _admin_required():
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        pw = request.form.get("password", "")
        if pw == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))
        flash("Contraseña incorrecta.", "error")

    return render_template("admin/login.html")


@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/dashboard")
def dashboard():
    if not _admin_required():
        return redirect(url_for("admin.login"))
    users = User.list_all()
    return render_template("admin/dashboard.html", users=users)


@admin_bp.route("/reset/<callsign>", methods=["POST"])
def reset_password(callsign):
    if not _admin_required():
        return redirect(url_for("admin.login"))

    token = User.generate_reset_token(callsign)
    if not token:
        flash(f"Usuario {callsign} no encontrado.", "error")
        return redirect(url_for("admin.dashboard"))

    flash(f"Token generado para {callsign}. Copiá el link de abajo.", "info")
    return render_template("admin/reset_link.html", callsign=callsign, token=token)


@admin_bp.route("/delete/<callsign>", methods=["POST"])
def delete_user(callsign):
    if not _admin_required():
        return redirect(url_for("admin.login"))

    User.delete(callsign)
    flash(f"Usuario {callsign} eliminado del sistema de auth. Sus contactos se mantienen.", "info")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/create", methods=["GET", "POST"])
def create_user():
    if not _admin_required():
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        callsign = request.form.get("callsign", "").strip().upper()
        password = request.form.get("password", "")
        if not callsign or not password:
            flash("Callsign y contraseña requeridos.", "error")
            return render_template("admin/create_user.html")
        user = User.register(callsign, password)
        if user is None:
            flash(f"{callsign} ya existe.", "error")
            return render_template("admin/create_user.html")
        flash(f"Usuario {callsign} creado correctamente.", "info")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/create_user.html")
