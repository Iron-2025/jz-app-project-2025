import os
import sys
import subprocess
import shutil
from pathlib import Path

def setup_project():
    """
    Set up the project by:
    1. Creating a virtual environment
    2. Installing dependencies
    3. Initializing the database
    4. Migrating data from the old database (if it exists)
    """
    print("Setting up Job Application Tracker...")
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)
    
    # Create virtual environment
    print("\nCreating virtual environment...")
    if sys.platform == 'win32':
        venv_cmd = [sys.executable, '-m', 'venv', 'venv']
    else:
        venv_cmd = ['python3', '-m', 'venv', 'venv']
    
    try:
        subprocess.run(venv_cmd, check=True)
        print("Virtual environment created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return
    
    # Activate virtual environment and install dependencies
    print("\nInstalling dependencies...")
    if sys.platform == 'win32':
        pip_cmd = [os.path.join('venv', 'Scripts', 'pip')]
    else:
        pip_cmd = [os.path.join('venv', 'bin', 'pip')]
    
    pip_cmd.extend(['install', '-r', 'requirements.txt'])
    
    try:
        subprocess.run(pip_cmd, check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return
    
    # Initialize the database
    print("\nInitializing database...")
    if sys.platform == 'win32':
        flask_cmd = [os.path.join('venv', 'Scripts', 'flask')]
    else:
        flask_cmd = [os.path.join('venv', 'bin', 'flask')]
    
    flask_cmd.extend(['--app', 'wsgi.py', 'init-db'])
    
    try:
        subprocess.run(flask_cmd, check=True)
        print("Database initialized successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing database: {e}")
        return
    
    # Migrate data from old database if it exists
    old_db_path = os.path.join('instance', 'job_tracker.db.bak')
    if os.path.exists(old_db_path):
        print("\nMigrating data from old database...")
        if sys.platform == 'win32':
            python_cmd = [os.path.join('venv', 'Scripts', 'python')]
        else:
            python_cmd = [os.path.join('venv', 'bin', 'python')]
        
        python_cmd.extend(['migrations/migrate_data.py'])
        
        try:
            subprocess.run(python_cmd, check=True)
            print("Data migration completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error migrating data: {e}")
    
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    if sys.platform == 'win32':
        print("1. Activate the virtual environment: venv\\Scripts\\activate")
        print("2. Start the Flask server: flask --app wsgi.py run")
    else:
        print("1. Activate the virtual environment: source venv/bin/activate")
        print("2. Start the Flask server: flask --app wsgi.py run")
    print("3. Open your browser and navigate to http://127.0.0.1:5000/")
    print("\nDefault login credentials:")
    print("Email: demo@example.com")
    print("Password: password")

if __name__ == '__main__':
    setup_project()
