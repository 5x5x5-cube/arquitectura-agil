from flask import Flask, jsonify, request
import requests
import os
from monitor import get_system_health
from security.auth import authenticate, validate_token, roles_required, get_token_payload

app = Flask(__name__)

# Order service URL from environment variable
ORDER_SERVICE_URL = os.environ.get("ORDER_SERVICE", "http://localhost:5000")

@app.route('/')
def hello_world():
    return 'Hello from API Gateway!'

@app.route('/health-checker')
def health_check():
    return jsonify(get_system_health())

@app.route('/auth', methods=['POST'])
def auth():
    return authenticate(request.json)

@app.route('/validate-token', methods=['POST'])
def token_validation():
    data = request.json
    print('data', data)
    
    # Check for required fields
    if not data or 'token' not in data or 'allowed_roles' not in data:
        return jsonify({"error": "Missing token or allowed_roles"}), 400
        
    # Validate token and check roles
    return validate_token(data['token'], data['allowed_roles'])


# Order service endpoints
@app.route('/orders', methods=['POST'])
@roles_required(['user', 'admin'])
def create_order():
    # Use the userId set as an attribute by the decorator
    user_id = getattr(request, 'userId', request.headers.get('userId'))
    
    # Create headers with userId
    headers = {'userId': str(user_id)} if user_id else {}
    
    # Also pass the user's role for additional validation if needed
    auth_header = request.headers.get('Authorization')
    if (auth_header and auth_header.startswith('Bearer ')):
        token = auth_header.split(' ')[1]
        payload_response = get_token_payload(token)
        if payload_response.status_code == 200:
            try:
                payload_data = payload_response.get_json()
                if payload_data and 'payload' in payload_data and 'roles' in payload_data['payload']:
                    headers['userRole'] = ','.join(payload_data['payload']['roles'])
            except Exception as e:
                app.logger.error(f"Error extracting roles from token: {str(e)}")
    
    response = requests.post(
        f"{ORDER_SERVICE_URL}/orders",
        json=request.json,
        headers=headers
    )
    return jsonify(response.json()), response.status_code

@app.route('/orders', methods=['GET'])
@roles_required(['admin'])
def get_all_orders():
    response = requests.get(f"{ORDER_SERVICE_URL}/orders")
    return jsonify(response.json()), response.status_code

@app.route('/orders/user', methods=['GET'])
@roles_required(['user', 'admin'])
def get_user_orders():
    # Use the userId set as an attribute by the decorator
    user_id = getattr(request, 'userId', request.headers.get('userId'))
    
    # Create headers with userId
    headers = {'userId': str(user_id)} if user_id else {}
    
    # Also pass the user's role for additional validation if needed
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        payload_response = get_token_payload(token)
        if payload_response.status_code == 200:
            try:
                payload_data = payload_response.get_json()
                if payload_data and 'payload' in payload_data and 'roles' in payload_data['payload']:
                    headers['userRole'] = ','.join(payload_data['payload']['roles'])
            except Exception as e:
                app.logger.error(f"Error extracting roles from token: {str(e)}")
    
    response = requests.get(
        f"{ORDER_SERVICE_URL}/orders/user",
        headers=headers
    )
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)