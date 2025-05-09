import pytest
# from dnd_rag import db, rag
from dnd_rag.model import Query
from dnd_rag.query_history import log_query


def log_query_direct(session):
    """Test that a LogItem can be created and saved using the session fixture."""
    # Arrange: Create a new LogItem instance using the imported model
    
    # Act: Add and commit the item using the provided session fixture
    log_query("What type of damage does a young black dragon's breath weapon do?","A yuong black dragon's breath weapon deals acid damage")

    # Assert: Query the database using the session fixture and check if the item exists
    # Use session.get() for primary key lookup (more efficient)
    all_queries = session.query(Query).all()

    # Verify the item was retrieved
    assert all_queries is not None

    assert len(all_queries) == 1


