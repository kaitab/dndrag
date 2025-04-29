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
    #user_query = request.form[""]
    return render_template("mainpage.html")

if __name__ == '__main__':
    build_rag()
    app.run(debug=True)
