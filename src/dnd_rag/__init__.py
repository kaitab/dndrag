from flask import Flask,  request, render_template
from flask_sqlalchemy import SQLAlchemy
from .dndRag import RAG
from os import path
from dnd_rag.query_history import log_query, all_queries

db = SQLAlchemy()
rag = None


def create_app():
    app = Flask(__name__)
    # app.config.from_object()

    home_directory = path.abspath(path.dirname(__file__))
    instance_sub_dir = path.join('instance', 'db.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{path.join(home_directory, instance_sub_dir)}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    global rag
    rag = RAG()

    @app.route("/", methods=["GET", "POST"])
    def main_page():
        """generates the main page"""
        if request.method == "GET":
            return render_template("mainpage.html", response="An answer will appear here with the roll of a die...")
        if request.method == "POST":
            try:
                query = request.form.get('user_query')
                rag_query = rag.query(query)
                ai_message = rag_query[-1]
                response = ai_message.content
                # log_query(rag_query, response)

                return render_template("mainpage.html", response=response)
            except Exception as e:
                print(e)
                return render_template("mainpage.html", response="Looks like we rolled a Nat 1! Something went wrong on our end, so please try again")

    return app

