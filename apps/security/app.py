from flask import Flask, request, jsonify
from auth import authenticate_user, generate_token
from models import db, init_db
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Flag to check if initialization has been done
initialized = False

@app.route('/')
def hello():
    return 'Security Service is running!'

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    user = authenticate_user(username, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = generate_token(user)
    return jsonify({'token': token, 'user_id': user.id})

@app.before_request
def create_tables():
    global initialized
    if not initialized:
        # Create tables and initialize with default users
        db.create_all()
        init_db()
        initialized = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
