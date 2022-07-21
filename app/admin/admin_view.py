from flask_admin.contrib.sqla import ModelView
from app.models.models import db, admin, User, Data

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Data, db.session))