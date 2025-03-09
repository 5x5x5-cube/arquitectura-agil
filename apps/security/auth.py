import jwt
import datetime
from models import get_user_by_username
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
        'username': user.username
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
