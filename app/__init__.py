from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


database = SQLAlchemy()


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    database.init_app(app)

    from blueprints.excel import excel
    app.register_blueprint(excel)

    from blueprints.users import users
    app.register_blueprint(users)

    with app.app_context():
        database.drop_all()
        database.create_all()

    return app
