import jwt
import datetime
from models import get_user_by_username, get_user_by_id
from flask import current_app

def authenticate_user(username, password):
    """Authenticate a user by username and password"""
    user = get_user_by_username(username)
    if user and user.password == password:  # In production, use password hashing!
        return user
    return None

def generate_token(user):
    """Generate a JWT token for authenticated user"""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow(),
        'sub': user.id,
        'username': user.username,
        'roles': [user.role]  
    }
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )

def validate_token(token):
    """Validate a JWT token"""
    try:
        payload = jwt.decode(
            token,
            current_app.config.get('SECRET_KEY'),
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def validate_token_and_roles(token, allowed_roles):
    """
    Validates a token and checks if the user has any of the allowed roles
    
    Args:
        token (str): The authentication token to validate
        allowed_roles (list): List of roles that are allowed to access the resource
        
    Returns:
        dict: The decoded token if valid and has proper roles, None otherwise
    """
    # Validate the token first
    payload = validate_token(token)
    print('payload', payload)
    if not payload:
        return None
    
    # Check if the user has any of the allowed roles
    user_roles = payload.get('roles', [])
    
    # If no roles are required, just return the validated token
    if not allowed_roles:
        return payload
    
    # Check if any of the user's roles match the allowed roles
    if any(role in allowed_roles for role in user_roles):
        return payload
    
    # User doesn't have any of the required roles
    return None
