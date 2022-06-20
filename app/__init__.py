from flask import Flask
from config import DevelopmentConfig
from flask_cors import CORS

cors = CORS()

# import extensions instance
from app.models import db, admin, migrate

def create_app(config=DevelopmentConfig, admin=admin):
    app = Flask(__name__)
    app.config.from_object(config)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    

    # initialize extension instances
    db.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)
    db.app = app
    
    # register blueprints of applications
    from app.main import main as main_bp
    app.register_blueprint(main_bp, url_prefix='/')


    # register blueprints of applications
    from app.admin import admin as admin_bp
    app.register_blueprint(admin_bp)
   
    return app