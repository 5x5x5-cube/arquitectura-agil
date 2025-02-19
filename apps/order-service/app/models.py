from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    product = db.Column(db.String(100), nullable=False)
