from flask import Flask, request, jsonify
from auth import authenticate_user, generate_token, validate_token_and_roles, validate_token
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

@app.route('/validate-token', methods=['POST'])
def validate_token_endpoint():
    data = request.get_json()
    
    if not data or 'token' not in data:
        return jsonify({'error': 'Missing token'}), 400
    
    # Extract token and allowed roles
    token = data['token']
    allowed_roles = data.get('allowed_roles', [])
    
    # Validate token and check roles
    payload = validate_token_and_roles(token, allowed_roles)
    
    
    if not payload:
        return jsonify({'valid': False, 'error': 'Invalid token'}), 401
    
    # Check if payload contains an 'invalid_role' flag
    if payload.get('invalid_role', False):
        return jsonify({'valid': False, 'error': 'Insufficient permissions'}), 403
    
    # Return the validated token payload with a valid flag
    response_data = {'valid': True, 'user_id': payload['sub'], 'username': payload['username']}
    
    # Include roles information if available
    if 'roles' in payload:
        response_data['roles'] = payload['roles']
        
    return jsonify(response_data)

@app.route('/token-payload', methods=['POST'])
def get_token_payload():
    """Endpoint that returns the decoded token payload"""
    # Get token from request - either from JSON body or Authorization header
    token = None
    data = request.get_json()
    
    if data and 'token' in data:
        token = data['token']
    else:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    
    if not token:
        return jsonify({'error': 'Missing token. Provide it in request body or Authorization header'}), 400
    
    # Validate the token
    payload = validate_token(token)
    
    if not payload:
        return jsonify({'error': 'Invalid or expired token'}), 401
    
    # Return the token payload
    return jsonify({'payload': payload})

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
