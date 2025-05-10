import pytest
from app.model import Query
from dnd_rag.query_history import log_query, all_queries, clear_query_history


def test_log_query_direct(session):
    """Tests that db is modified/access when using query_history functions"""

    log_query("What type of damage does a young black dragon's breath weapon do?","A young black dragon's breath weapon deals acid damage")

    logged_queries = session.query(Query).all()

    # check first item is added

    assert logged_queries is not None
    assert len(logged_queries) == 1
    assert len(logged_queries) == len(all_queries())

    log_query("What type of damage does an adult gold dragon's breath weapon do?", "An adult gold dragon's breath weapon deals fire damage")

    # check 2nd item is added

    logged_queries = session.query(Query).all()
    updated_list = all_queries()
    assert len(logged_queries) == 2
    assert len(logged_queries) == len(updated_list)
    assert "black dragon" in updated_list[0]["content"] and "black dragon" in updated_list[0]["reply"]
    assert "gold dragon" in updated_list[1]["content"] and "gold dragon" in updated_list[1]["reply"]


def test_log_query_via_post(client, session):
    """Tests that db is updated when a POST request is made"""

    form_data = {
        "user_query": "What is the alignment of a Beholder?",
        "submit": "Make a history check"
    }
    response = client.post('/', data=form_data)
    assert b"404" not in response.data  
    
    queries_ist = session.query(Query).all()

    assert queries_ist is not None

    assert len(queries_ist) == 1


def test_clear_history(client, session):
    """Tests that entries can be cleared from db"""

    log_query("What type of damage does a young black dragon's breath weapon do?","A young black dragon's breath weapon deals acid damage")

    logged_queries = session.query(Query).all()

    # check first item is added

    assert logged_queries is not None
    assert len(logged_queries) == 1
    assert len(logged_queries) == len(all_queries())

    clear_query_history()
    # check that it is now removed
    logged_queries = session.query(Query).all()
    assert len(logged_queries) == len(all_queries()) == 0


def test_clear_history_post(client, session):
    """Tests that entries can be cleared from db"""

    log_query("What type of damage does a young black dragon's breath weapon do?","A young black dragon's breath weapon deals acid damage")

    assert len(session.query(Query).all()) == 1
    assert len(session.query(Query).all()) == len(all_queries())

    response = client.post('/clear')

    assert b"404" not in response.data 
    assert len(session.query(Query).all()) == 0
