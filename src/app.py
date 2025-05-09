from dnd_rag import create_app
# app = Flask(__name__)

# # def make_rag():
# #     global rag
# #     rag = RAG()

# rag = RAG()



if __name__ == '__main__':
    # make_rag() # method 1, still runs initilization twice this way
    app = create_app()
    app.run(debug=True, use_reloader=True, reloader_type='stat')
