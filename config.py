import os
from dotenv import load_dotenv
#Load ENV variables
load_dotenv('.flaskenv')

APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True   
    # Chemin SQL Alchemy
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{APPLICATION_DIR}/mushrooms.sqlite"
    #SQLALCHEMY_DATABASE_URI = "postgresql://postgres:secretpassword@localhost:5432/blob.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Create the testing config
class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{APPLICATION_DIR}/mushrooms.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False