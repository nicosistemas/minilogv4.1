from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user

from models.users import User, _load_db, _save_db
from werkzeug.security import check_password_hash, generate_password_hash

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_pw  = request.form.get("current_password", "")
        new_pw      = request.form.get("new_password", "")
        confirm_pw  = request.form.get("confirm_password", "")

        if not current_pw or not new_pw:
            flash("Completá todos los campos.", "error")
            return render_template("change_password.html")

        if new_pw != confirm_pw:
            flash("Las contraseñas nuevas no coinciden.", "error")
            return render_template("change_password.html")

        if len(new_pw) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "error")
            return render_template("change_password.html")

        db = _load_db()
        if not check_password_hash(db[current_user.id], current_pw):
            flash("La contraseña actual es incorrecta.", "error")
            return render_template("change_password.html")

        db[current_user.id] = generate_password_hash(new_pw)
        _save_db(db)

        flash("Contraseña actualizada correctamente.", "info")
        return redirect(url_for("main.index"))

    return render_template("change_password.html")
