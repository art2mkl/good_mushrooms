from flask_admin.contrib.sqla import ModelView
from app.models import db, admin, User

admin.add_view(ModelView(User, db.session))