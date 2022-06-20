import pytest

from app import create_app
from config import TestingConfig
from flask_admin import Admin

@pytest.fixture
def client():

    admin = Admin(name='my-app', template_mode='bootstrap3')
    app = create_app(TestingConfig, admin)
    with app.test_client() as client:
        yield client