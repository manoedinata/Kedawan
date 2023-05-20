from flask import Flask

from flask_migrate import Migrate

from dotenv import dotenv_values

from kedawan.db import db

from kedawan.api.main_api import main_api_bp as main_api
from kedawan.api.fastadd_api import fastadd_api_bp as fastadd_api

from kedawan.webui.main_webui import main_webui

config = dotenv_values(".env") 

migrate = Migrate()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["BUNDLE_ERRORS"] = True

    # DB
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        f"mariadb://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_HOST']}:{config.get('DB_PORT', 3306)}/{config['DB_NAME']}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # API
    app.register_blueprint(main_api, url_prefix="/api")
    app.register_blueprint(fastadd_api, url_prefix="/api")

    # Web UI
    app.register_blueprint(main_webui, url_prefix="/")

    @app.context_processor
    def add_jinja_vars():
        return config

    return app
