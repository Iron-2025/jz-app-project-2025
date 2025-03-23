from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from app.core.db import get_db
from datetime import datetime

class User(UserMixin):
    """User model for authentication and user management."""
    
    def __init__(self, id, email, password_hash, name=None, created_at=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.created_at = created_at
    
    @staticmethod
    def get_by_id(user_id):
        """Retrieve a user by ID."""
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
        if user is None:
            return None
        
        return User(
            id=user['id'],
            email=user['email'],
            password_hash=user['password'],
            name=user['name'],
            created_at=user['created_at']
        )
    
    @staticmethod
    def get_by_email(email):
        """Retrieve a user by email."""
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()
        
        if user is None:
            return None
        
        return User(
            id=user['id'],
            email=user['email'],
            password_hash=user['password'],
            name=user['name'],
            created_at=user['created_at']
        )
    
    @staticmethod
    def create(email, password, name=None):
        """Create a new user."""
        db = get_db()
        
        # Check if user already exists
        if User.get_by_email(email) is not None:
            return None
        
        # Create new user
        db.execute(
            'INSERT INTO user (email, password, name) VALUES (?, ?, ?)',
            (email, generate_password_hash(password), name)
        )
        db.commit()
        
        # Return the newly created user
        return User.get_by_email(email)
    
    def update_profile(self, name=None, email=None):
        """Update user profile information."""
        db = get_db()
        
        # If email is being changed, check if it's already in use
        if email and email != self.email:
            existing_user = User.get_by_email(email)
            if existing_user is not None:
                return False, "Email already in use"
        
        # Update user information
        db.execute(
            'UPDATE user SET name = ?, email = ? WHERE id = ?',
            (name or self.name, email or self.email, self.id)
        )
        db.commit()
        
        # Update object attributes
        self.name = name or self.name
        self.email = email or self.email
        
        return True, "Profile updated successfully"
    
    def change_password(self, current_password, new_password):
        """Change user password."""
        # Verify current password
        if not self.check_password(current_password):
            return False, "Current password is incorrect"
        
        # Update password
        db = get_db()
        db.execute(
            'UPDATE user SET password = ? WHERE id = ?',
            (generate_password_hash(new_password), self.id)
        )
        db.commit()
        
        # Update object attribute
        self.password_hash = generate_password_hash(new_password)
        
        return True, "Password changed successfully"
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def format_created_at(self):
        """Format the created_at timestamp in a user-friendly way."""
        if not self.created_at:
            return "N/A"
        
        try:
            # Try to parse the timestamp directly
            if isinstance(self.created_at, str):
                # Handle ISO format with Z
                if 'Z' in self.created_at:
                    timestamp = self.created_at.replace('Z', '+00:00')
                    dt = datetime.fromisoformat(timestamp)
                else:
                    # Try to parse as is
                    dt = datetime.fromisoformat(self.created_at)
            else:
                # If it's already a datetime object
                dt = self.created_at
                
            return dt.strftime("%B %d, %Y")
        except (ValueError, TypeError, AttributeError):
            # If parsing fails, return the raw value
            return str(self.created_at)

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback."""
    return User.get_by_id(int(user_id))
