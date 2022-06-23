# import and register blueprints
from flask import Blueprint

exploration = Blueprint('exploration', __name__, template_folder='templates' )

# import any flask extension specific to this module

# import views
from app.exploration import exploration_views