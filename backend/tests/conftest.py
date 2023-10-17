# conftest.py

import pytest
from ..app import create_app
from ..database import db as _db

@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for each test."""
    # Create a test client using the Flask application configured for testing
    app = create_app(testing=True)

    # Establish an application context
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='session')
def db(app):
    """Create the test database tables."""
    with app.app_context():
        # Ensure the Flask app context is correctly set up
        db.app = app
        # Create the test database tables
        _db.create_all()
        yield _db
        # Drop the test database tables after tests are done
        _db.drop_all()
