from flask import Flask, request, jsonify
from models import db, Order
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Flag to check if initialization has been done
initialized = False

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = request.headers.get('userId')
    if not user_id:
        return jsonify({"error": "Missing userId header"}), 400
    new_order = Order(
        date=data["date"],
        product=data["product"],
        userId=user_id
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order Created"}), 201

@app.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "date": o.date, "product": o.product, "userId": o.userId} for o in orders])

@app.route("/orders/user", methods=["GET"])
def get_orders_by_user():
    user_id = request.headers.get('userId')
    if not user_id:
        return jsonify({"error": "Missing userId header"}), 400
    
    orders = Order.query.filter_by(userId=user_id).all()
    return jsonify([{"id": o.id, "date": o.date, "product": o.product, "userId": o.userId} for o in orders])

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"message":"Service orders is OK"})


@app.before_request
def create_tables():
    global initialized
    if not initialized:
        # Create tables and initialize with default users
        db.create_all()
        initialized = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)