from flask import Flask
from flask_migrate import Migrate
from config import DevelopmentConfig

# import extensions instance
from app.models import db


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    # initialize extension instances
    db.init_app(app)
    db.app = app

    # register blueprints of applications
    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    # register blueprints of applications
    # from app.main import main as main_bp
    # app.register_blueprint(main_bp, url_prefix='/main')

    return app