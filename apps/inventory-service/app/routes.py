from flask import Blueprint, jsonify, request
from app import db
from app.models import Inventory

api_bp = Blueprint("api", __name__)


@api_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    new_product = Inventory(
        name=data["name"],
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product Created"}), 201


@api_bp.route("/products", methods=["GET"])
def get_products():
    products = Inventory.query.all()
    return jsonify(
        [{"id": p.id, "name": p.name, "available": p.available} for p in products]
    )


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"message": "Service inventory is OK"})
