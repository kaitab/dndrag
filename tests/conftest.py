import pytest
from app import create_app, db

@pytest.fixture(scope='session')
def app_and_rag_context():
    """Session-wide test application."""
    
    app, rag = create_app(testing=True)

    context = app.app_context()
    context.push()

    # Yield the app instance to the tests
    yield app, rag

    # Clean up the context after the tests are done
    context.pop()

@pytest.fixture(scope='session')
def app(app_and_rag_context):
    """Fixture to provide the app instance."""
    return app_and_rag_context[0]

@pytest.fixture(scope='session')
def rag(app_and_rag_context):
    """Fixture to provide the rag instance."""
    return app_and_rag_context[1] 


@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    # The client fixture automatically works within the app context
    # It allows simulating requests to the Flask app
    return app.test_client()

@pytest.fixture(scope='function')
def database(app):
    """Fixture to provide a clean database for each test function."""
    # Ensure we are within the application context
    with app.app_context():
        # Create all tables defined in the models
        db.create_all()

        # Yield the db instance to the tests
        yield db

        # Drop all tables after the test function finishes
        # This cleans up the database for the next test
        db.drop_all()

@pytest.fixture(scope='function')
def session(database):
    """Fixture to provide a database session for each test function."""
    # Use the session provided by SQLAlchemy
    # This session is tied to the in-memory database created by the 'database' fixture
    yield database.session
