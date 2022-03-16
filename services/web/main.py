import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)

    from routes import auth, common
    app.register_blueprint(auth.auth_routes)
    app.register_blueprint(common.common_routes)

    app.secret_key = os.urandom(10)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

