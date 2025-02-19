from flask import Blueprint, jsonify
from app import db

api_bp = Blueprint("api", __name__)


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"message":"Service inventory is OK"})
