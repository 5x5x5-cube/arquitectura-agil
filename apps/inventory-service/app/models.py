from app import db


class Inventory(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    available = db.Column(db.Boolean, nullable=False, default=True)
