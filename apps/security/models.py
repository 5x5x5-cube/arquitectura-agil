from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # In production, store hashed passwords!
    role = db.Column(db.String(20), nullable=False, default='user')

    def to_dict(self):
        """Convert user object to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

def get_user_by_username(username):
    """Find a user by username"""
    return User.query.filter_by(username=username).first()

def get_user_by_id(user_id):
    """Find a user by ID"""
    return User.query.get(user_id)

def init_db():
    """Initialize the database with default users"""
    # Check if users already exist
    if User.query.count() == 0:
        # Create default users
        default_users = [
            User(id='1', username='admin', password='admin123', role='admin'),
            User(id='2', username='user', password='user123', role='user')
        ]
        
        # Add to database
        for user in default_users:
            db.session.add(user)
        db.session.commit()
        print("Default users created in database.")
