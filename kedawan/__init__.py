from flask import Flask

from flask_migrate import Migrate

from kedawan.config import config

from kedawan.db import db

from kedawan.api.main_api import main_api_bp as main_api
from kedawan.api.fastadd_api import fastadd_api_bp as fastadd_api

from kedawan.webui.main_webui import main_webui


migrate = Migrate()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["BUNDLE_ERRORS"] = True

    # DB
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        f"mariadb://{config['MYSQL_USER']}:{config['MYSQL_PASSWORD']}@{config['MYSQL_HOST']}:{config.get('MYSQL_PORT', 3306)}/{config['MYSQL_DATABASE']}"
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
