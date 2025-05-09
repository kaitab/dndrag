from dnd_rag.model import Query, db
from datetime import datetime

def log_query(content: str, reply: str):
    new_query = Query(
            content=content,
            reply=reply,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
    db.session.add(new_query)
    db.session.commit()


def all_queries():
    queries = Query.query.all()
    data = [{'content': q.content, 'reply': q.reply, 'date': q.date} for q in queries]
    return data

