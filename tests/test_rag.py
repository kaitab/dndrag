import pytest

def test_rag_directly(rag):
    assert rag is not None

    result = rag.query('what skills are associated with the wisdom stat?')
            
    ai_message = result[-1].content
    assert (any(skill in ai_message.lower() for skill in ['animal handling','perception','insight','medicine']))

def test_rag_post(client, rag):
    assert rag is not None

    form_data = {
        "user_query": "What is the alignment of a Beholder?",
        "submit": "Make a history check"
    }
    response = client.post('/', data=form_data)
    assert b"404" not in response.data
            
    html_string = response.text.lower()

    if 'nat 1' not in html_string:
        assert (any(skill in html_string for skill in ['animal handling','perception','insight','medicine']))

