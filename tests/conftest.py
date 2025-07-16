import pytest

from app import app as flask_app
from models import db

@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    with flask_app.app_context():
        # setup
        db.create_all()
        yield flask_app
        # teardown
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()