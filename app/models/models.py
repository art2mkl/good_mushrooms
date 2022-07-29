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

    @staticmethod
    def exists(email):
        user = User.query.filter(User.email == email).first()
        if user:
            return True
        else:
            return False

 
#-------------------Model DATA-------------------
class Data(db.Model):

    _id = db.Column(db.Integer, primary_key=True)    
    _class = db.Column(db.String(64))
    _cap_shape = db.Column(db.String(64))
    _cap_surface = db.Column(db.String(64))
    _cap_color = db.Column(db.String(64))
    _bruises = db.Column(db.String(64))
    _odor = db.Column(db.String(64))
    _gill_attachment = db.Column(db.String(64))
    _gill_spacing = db.Column(db.String(64))
    _gill_size =  db.Column(db.String(64))
    _gill_color = db.Column(db.String(64))
    _stalk_shape = db.Column(db.String(64))
    _stalk_root = db.Column(db.String(64))
    _stalk_surface_above_ring = db.Column(db.String(64))
    _stalk_surface_below_ring = db.Column(db.String(64))
    _stalk_color_above_ring = db.Column(db.String(64))
    _stalk_color_below_ring = db.Column(db.String(64))
    _veil_type = db.Column(db.String(64))
    _veil_color = db.Column(db.String(64))
    _ring_number = db.Column(db.String(64))
    _ring_type = db.Column(db.String(64))
    _spore_print_color = db.Column(db.String(64))
    _population = db.Column(db.String(64))
    _habitat = db.Column(db.String(64))

class Ml(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(64))
    cols = db.Column(db.String())
    model = db.Column(db.String())
    parameters = db.Column(db.String())
    accuracy = db.Column(db.Float())
    precision = db.Column(db.Float())
    path = db.Column(db.String())
    display = db.Column(db.Boolean(), default=True)


