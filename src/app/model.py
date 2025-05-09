from . import db

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    reply = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(80), nullable=False)
