from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    product = db.Column(db.String(100), nullable=False)
    userId = db.Column(db.String(100), nullable=True)
