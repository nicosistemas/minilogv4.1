from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from models.users import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        callsign = request.form.get("callsign", "").strip().upper()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")

        if not callsign or not password:
            flash("Callsign y contraseña son requeridos.", "error")
            return render_template("register.html")

        if password != confirm:
            flash("Las contraseñas no coinciden.", "error")
            return render_template("register.html")

        user = User.register(callsign, password)
        if user is None:
            flash(f"El callsign {callsign} ya está registrado.", "error")
            return render_template("register.html")

        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        callsign = request.form.get("callsign", "").strip().upper()
        password = request.form.get("password", "")

        user = User.authenticate(callsign, password)
        if user is None:
            flash("Callsign o contraseña incorrectos.", "error")
            return render_template("login.html")

        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
