from . import rag
from flask import request, render_template, Blueprint
from dnd_rag.query_history import log_query, all_queries

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET", "POST"])
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
            log_query(query, response)

            return render_template("mainpage.html", response=response,history=all_queries())
        except Exception as e:
            print(e)
            return render_template("mainpage.html", response="Looks like we rolled a Nat 1! Something went wrong on our end, so please try again")
