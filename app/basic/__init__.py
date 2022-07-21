# import and register blueprints
from flask import Blueprint

basic = Blueprint('basic', __name__, template_folder='templates' )

# import views
from app.basic import basic_views