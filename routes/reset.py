from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.users import User

reset_bp = Blueprint("reset", __name__)


@reset_bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    callsign = User.validate_reset_token(token)
    if not callsign:
        return render_template("reset_invalid.html")

    if request.method == "POST":
        new_pw  = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")

        if not new_pw or len(new_pw) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "error")
            return render_template("reset_form.html", token=token, callsign=callsign)

        if new_pw != confirm:
            flash("Las contraseñas no coinciden.", "error")
            return render_template("reset_form.html", token=token, callsign=callsign)

        User.consume_reset_token(token, new_pw)
        flash("Contraseña actualizada. Ya podés iniciar sesión.", "info")
        return redirect(url_for("auth.login"))

    return render_template("reset_form.html", token=token, callsign=callsign)
