from flask import Blueprint, request, jsonify
from app import db
from app.models import Order

api_bp = Blueprint("api", __name__)

@api_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    new_order = Order(
        date=data["date"],
        product=data["product"],
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order Created"}), 201

@api_bp.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "date": o.date, "product": o.product} for o in orders])
