from flask import Flask, request, render_template
from dndRag import RAG


app = Flask(__name__)

# def make_rag():
#     global rag
#     rag = RAG()

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
            return render_template("mainpage.html", response=response)
        except Exception as e:
            print(e)
            return render_template("mainpage.html", response="Looks like we rolled a Nat 1! Something went wrong on our end, so please try again")
        

if __name__ == '__main__':
    # make_rag() # method 1, still runs initilization twice this way
    app.run(debug=True, use_reloader=True, reloader_type='stat')
