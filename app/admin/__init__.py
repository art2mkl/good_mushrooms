# import and register blueprints
from flask import Blueprint

admin = Blueprint('admin_bp', __name__)

# import any flask extension specific to this module

# import admin_view
from app.admin import admin_view