from flask import Flask,  request, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
rag = None


def create_app(testing=False):
    app = Flask(__name__)
    # app.config.from_object()

    home_directory = (path.dirname(__file__))
    src_dir = path.dirname(home_directory)
    instance_sub_dir = path.join('instance', 'db.sqlite')
    filename =  f"sqlite:///{path.join(src_dir, instance_sub_dir)}"
    app.config['SQLALCHEMY_DATABASE_URI'] = filename
    if testing:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True

    from dnd_rag.dndRag import RAG
    from dnd_rag.query_history import log_query, all_queries

    db.init_app(app)

    global rag
    rag = RAG()

    return app, rag

app, rag = create_app()

from app import model, routes

