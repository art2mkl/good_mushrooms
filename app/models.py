# import models extensions
import datetime
from flask_sqlalchemy import SQLAlchemy

# create an instance of the extension with initializing it
db = SQLAlchemy()

#-------------------Model USER-------------------
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(64))

    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

