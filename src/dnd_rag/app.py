from flask import Flask, request, render_template

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def main_page():
    """generates the main page"""
    #user_query = request.form[""]
    return render_template("mainpage.html")

if __name__ == '__main__':
    app.run(debug=True)
