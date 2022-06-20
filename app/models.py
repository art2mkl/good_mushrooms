# import models extensions
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# create an instance of the extension with initializing it
bcrypt = Bcrypt()

# create an instance of the extension with initializing it
db=SQLAlchemy()

# create an instance of the extension with initializing it
admin = Admin(name='MUSHROOM DB Admin', template_mode='bootstrap3')

# create an instance of the extension with initializing it
migrate = Migrate()



#-------------------Model USER-------------------
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(64))
    
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    
    # projects = db.relationship('Project', backref='user', lazy='dynamic')
    
    def __init__(self, name=None, email=None, password=None, *args, **kwargs):
    
        self.name = name
        self.email = email
        self.password = self.generate_hash(password)

    def generate_hash(self, password):
        if self.email:
            return bcrypt.generate_password_hash(password)
        
    def check_hash(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)

    def get_id(self):  
        return self.id

    def __repr__(self):
        return '<User %r>' % self.email

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter(User.email == email).first()
        if user and user.check_hash(password):
            return user
        return False

    @staticmethod
    def load_session(email):
        user = User.query.filter(User.email == email).first()
        
        #Load session parameters
        if user :
            session['user'] = user.name
            session['id'] = user.id
            session['role'] = user.role

    @staticmethod
    def exists(email):
        user = User.query.filter(User.email == email).first()
        if user:
            return True
        else:
            return False


