# import and register blueprints
from flask import Blueprint

prediction = Blueprint('prediction', __name__, template_folder='templates' )

# import views
from app.prediction import prediction_views