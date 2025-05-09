from app import app,  db

if __name__ == '__main__':
    # make_rag() # method 1, still runs initilization twice this way
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True, use_reloader=True, reloader_type='stat')
