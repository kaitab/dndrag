from flask import Flask, request, render_template
from langchain_tutorial import RAG
app = Flask(__name__)
rag = RAG()

def build_rag():
    global rag 
    rag = RAG()

@app.route("/", methods=["GET", "POST"])
def main_page():
    """generates the main page"""
    if request.method == "GET":
        return render_template("mainpage.html", response="An answer will appear here with the roll of a die...")
    if request.method == "POST":
        query = request.args["user_query"]
        return render_template("mainpage.html", response=rag.query(query)["AI Message"])

if __name__ == '__main__':
    build_rag()
    app.run(debug=True)
