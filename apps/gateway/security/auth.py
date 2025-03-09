import requests
from flask import Response, jsonify, request
from functools import wraps

# Security service endpoint
SECURITY_SERVICE = 'http://localhost:5001'

def authenticate(auth_data):
    """
    Authenticates a user by calling the security service
    
    Args:
        auth_data (dict): The authentication data to send to the security service
        
    Returns:
        Flask Response object with the authentication result
    """
    try:
        response = requests.post(f"{SECURITY_SERVICE}/auth", json=auth_data)
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Security service unavailable"}), 503

def validate_token(token, allowed_roles):
    """
    Validates a token and checks if the user has any of the allowed roles
    
    Args:
        token (str): The authentication token to validate
        allowed_roles (list): List of roles that are allowed to access the resource
        
    Returns:
        Flask Response object with the validation result
    """
    try:
        # Call the security service to validate the token and check roles
        response = requests.post(
            f"{SECURITY_SERVICE}/validate-token", 
            json={"token": token, "allowed_roles": allowed_roles}
        )
        
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Security service unavailable"}), 503

def roles_required(allowed_roles):
    """
    Decorator that checks if the user has any of the required roles
    
    Args:
        allowed_roles (list): List of roles that are allowed to access the route
    
    Returns:
        Function: Decorated function that checks authorization
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get token from Authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({"error": "Authorization header missing or invalid"}), 401
            
            token = auth_header.split(' ')[1]
            
            # Validate token and check roles
            validation_response = validate_token(token, allowed_roles)
            
            # If validation failed, return the error response
            if validation_response.status_code != 200:
                return validation_response
                
            # If valid, proceed with the original route function
            return f(*args, **kwargs)
        return decorated_function
    return decorator
