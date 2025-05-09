from dnd_rag import create_app,  db
# app = Flask(__name__)

# # def make_rag():
# #     global rag
# #     rag = RAG()

# rag = RAG()



if __name__ == '__main__':
    # make_rag() # method 1, still runs initilization twice this way
    app = create_app()
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True, use_reloader=True, reloader_type='stat')
