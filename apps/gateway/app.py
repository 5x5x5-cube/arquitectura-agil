from flask import Flask, jsonify, request
from monitor import get_system_health
from security.auth import authenticate, validate_token, roles_required

app = Flask(__name__)

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

# Example of a protected route using the decorator
@app.route('/protected-admin', methods=['GET'])
@roles_required(['admin'])
def protected_admin():
    return jsonify({"message": "This is a protected endpoint for admins only"})

# Example with multiple allowed roles
@app.route('/protected-user', methods=['GET'])
@roles_required(['user'])
def protected_user():
    return jsonify({"message": "This endpoint is accessible to users and admins"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)