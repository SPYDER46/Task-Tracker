from flask import Flask
from flask_login import LoginManager
from .models import get_user_by_id

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    from .auth import auth_bp
    from .routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

    return app