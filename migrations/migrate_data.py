import os
import sqlite3
from werkzeug.security import generate_password_hash

def migrate_data():
    """
    Migrate data from the old database schema to the new one.
    This script:
    1. Creates a demo user if it doesn't exist
    2. Associates existing job applications with the demo user
    """
    print("Starting data migration...")
    
    # Get database paths
    old_db_path = os.path.join('instance', 'job_tracker.db')
    new_db_path = os.path.join('instance', 'job_tracker_new.db')
    
    # Check if old database exists
    if not os.path.exists(old_db_path):
        print(f"Old database not found at {old_db_path}")
        return
    
    # Connect to old database
    old_db = sqlite3.connect(old_db_path)
    old_db.row_factory = sqlite3.Row
    
    # Connect to new database
    new_db = sqlite3.connect(new_db_path)
    new_db.row_factory = sqlite3.Row
    
    try:
        # Create new schema
        with open('app/core/schema.sql', 'r') as f:
            new_db.executescript(f.read())
        
        # Get demo user ID
        user_id = new_db.execute('SELECT id FROM user WHERE email = ?', ('demo@example.com',)).fetchone()
        
        if user_id:
            user_id = user_id['id']
        else:
            # Create demo user if it doesn't exist
            cursor = new_db.execute(
                'INSERT INTO user (email, password, name) VALUES (?, ?, ?)',
                ('demo@example.com', generate_password_hash('password'), 'Demo User')
            )
            user_id = cursor.lastrowid
            new_db.commit()
        
        # Get existing job applications
        applications = old_db.execute('SELECT * FROM job_application').fetchall()
        
        if applications:
            print(f"Found {len(applications)} job applications to migrate")
            
            # Migrate job applications
            for app in applications:
                new_db.execute(
                    '''
                    INSERT INTO job_application 
                    (user_id, company, role, date_applied, status, notes) 
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (
                        user_id,
                        app['company'],
                        app['role'],
                        app['date_applied'],
                        app['status'],
                        app['notes']
                    )
                )
            
            new_db.commit()
            print(f"Successfully migrated {len(applications)} job applications")
        else:
            print("No job applications found to migrate")
        
        # Rename databases
        new_db.close()
        old_db.close()
        
        # Backup old database
        os.rename(old_db_path, f"{old_db_path}.bak")
        
        # Move new database to replace old one
        os.rename(new_db_path, old_db_path)
        
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        # Clean up
        new_db.close()
        old_db.close()
        
        # Remove new database if it exists
        if os.path.exists(new_db_path):
            os.remove(new_db_path)

if __name__ == '__main__':
    migrate_data()
