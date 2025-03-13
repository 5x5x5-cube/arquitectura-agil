import requests
import os
from flask import Response, jsonify, request
from functools import wraps
from logger import Logger

# Security service endpoint from environment variable
SECURITY_SERVICE = os.environ.get("SECURITY_SERVICE", "http://localhost:5001")

# Initialize logger
logger = Logger("gateway_auth.log")

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
        if response.status_code != 200:
            logger.error("Authentication failed via gateway", 
                         {"username": auth_data.get('username'), 
                          "status_code": response.status_code,
                          "ip": request.remote_addr})
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
    except requests.exceptions.ConnectionError:
        logger.error("Security service unavailable during authentication", 
                     {"ip": request.remote_addr})
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
        
        if response.status_code != 200:
            logger.error("Token validation failed via gateway", 
                        {"allowed_roles": allowed_roles, 
                         "status_code": response.status_code,
                         "ip": request.remote_addr})
        
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
    except requests.exceptions.ConnectionError:
        logger.error("Security service unavailable during token validation", 
                    {"ip": request.remote_addr})
        return jsonify({"error": "Security service unavailable"}), 503

def get_token_payload(token):
    """
    Retrieves the decoded payload of a JWT token by calling the security service
    
    Args:
        token (str): The authentication token to decode
        
    Returns:
        Flask Response object with the token payload
    """
    try:
        # Call the security service to get the token payload
        response = requests.post(
            f"{SECURITY_SERVICE}/token-payload", 
            json={"token": token}
        )
        
        if response.status_code != 200:
            logger.error("Failed to decode token via gateway", 
                        {"status_code": response.status_code,
                         "ip": request.remote_addr})
        
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
    except requests.exceptions.ConnectionError:
        logger.error("Security service unavailable during token decoding", 
                    {"ip": request.remote_addr})
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
                logger.error("Authorization failed: Missing or invalid header", 
                           {"ip": request.remote_addr, 
                            "path": request.path,
                            "required_roles": allowed_roles})
                return jsonify({"error": "Authorization header missing or invalid"}), 401
            
            token = auth_header.split(' ')[1]
            
            # Validate token and check roles
            validation_response = validate_token(token, allowed_roles)
            
            # If validation failed, return the error response
            if validation_response.status_code != 200:
                if validation_response.status_code == 403:
                    logger.error("Authorization failed: Insufficient permissions", 
                               {"ip": request.remote_addr, 
                                "path": request.path,
                                "required_roles": allowed_roles})
                    
                elif validation_response.status_code == 401:
                    logger.error("Authorization failed: Invalid token", 
                               {"ip": request.remote_addr, 
                                "path": request.path})

                return validation_response
            
            # If validation is successful and 'user' role is in allowed_roles
            if 'user' in allowed_roles:
                # Get token payload
                payload_response = get_token_payload(token)
                
                # If payload retrieval is successful
                if payload_response.status_code == 200:
                    try:
                        # Extract payload data
                        payload_data = payload_response.get_json()
                        if payload_data and 'payload' in payload_data and 'sub' in payload_data['payload'] and 'user' in payload_data['payload']['roles']:
                            # Add userId to request headers
                            user_id = payload_data['payload']['sub']
                            # Flask's request object doesn't allow directly modifying headers
                            # So we add it to an internal attribute that can be accessed later
                            if not hasattr(request, 'userId'):
                                setattr(request, 'userId', user_id)
                            logger.info(f"Added userId header: {user_id}", 
                                      {"path": request.path})
                    except Exception as e:
                        logger.error(f"Error extracting user ID from token payload: {str(e)}", 
                                    {"path": request.path})
                
            # If valid, proceed with the original route function
            return f(*args, **kwargs)
        return decorated_function
    return decorator
