-- Drop tables if they exist
DROP TABLE IF EXISTS job_application;
DROP TABLE IF EXISTS user;

-- Create user table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create job_application table with user_id foreign key
CREATE TABLE job_application (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    date_applied TEXT NOT NULL,
    status TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Insert sample user data
INSERT INTO user (email, password, name)
VALUES 
    ('demo@example.com', 'pbkdf2:sha256:150000$GJhgw2Z4$1a1d8be4bae4d28c5c8f5f0fe7a7b13d88a7bc614fd5a61762fa5b5b98e9489e', 'Demo User');

-- Insert sample job application data
INSERT INTO job_application (user_id, company, role, date_applied, status, notes)
VALUES 
    (1, 'Google', 'Software Engineer', '2025-03-01', 'Applied', 'Applied through company website'),
    (1, 'Microsoft', 'Frontend Developer', '2025-03-05', 'Interviewing', 'First interview scheduled for next week'),
    (1, 'Amazon', 'Full Stack Developer', '2025-02-20', 'Rejected', 'Received rejection email on March 10');
