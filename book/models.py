from dbs import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    content = db.Column(db.String(350), nullable=False)
