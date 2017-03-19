from flask import Flask
from config import config_types
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(config="dev"):
    app = Flask(__name__)
    app.config.from_object(config_types[config])

    db.init_app(app)

    from .site import main
    app.register_blueprint(main)

    login_manager.init_app(app)
    global bcrypt
    bcrypt = Bcrypt(app)

    with app.app_context():
        #db.drop_all()
        db.create_all()


    return app
