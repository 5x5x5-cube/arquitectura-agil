import requests
from flask import Response, jsonify

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
