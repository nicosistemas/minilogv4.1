from flask import Flask
from flask_login import LoginManager

from config import SECRET_KEY
from models.users import User
from routes.auth import auth_bp
from routes.main import main_bp
from routes.export import export_bp
from routes.lookup import lookup_bp
from routes.api import api_bp
from routes.profile import profile_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    # Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Iniciá sesión para acceder al log."
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.get(user_id)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(lookup_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(profile_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
