from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__, instance_relative_config=True)
    
    # Set default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'default-secret-key'),
        DATABASE=os.path.join(app.instance_path, 'job_tracker.db'),
    )
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    
    # Register database functions
    from app.core import db
    db.init_app(app)
    
    # Register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.job_tracker import job_tracker as job_tracker_blueprint
    app.register_blueprint(job_tracker_blueprint, url_prefix='/job-tracker')
    
    from app.core import core as core_blueprint
    app.register_blueprint(core_blueprint)
    
    return app
