# Job Application Tracker

A web application that helps job seekers track their job applications and monitor their status visually.

## Project Overview

This project is a web application built with Flask (Python) for the backend, SQLite for the database, and HTML/CSS/JavaScript for the frontend. It allows users to:

- Create an account and log in securely
- Add new job applications with details like company name, role, date applied, and status
- View all applications in either card or table format
- Filter applications by status
- Edit or delete existing applications
- Track the progress of job applications visually

## Features

- **User Authentication**
  - Secure signup and login system
  - Password hashing and protection
  - Session management
  - User profile page

- **Job Application Management**
  - Add, edit, and delete job applications
  - Track application status (Applied, Interviewing, Rejected, Offer, Accepted)
  - Filter applications by status
  - View applications in card or table format

- **Data Privacy**
  - Each user can only see and manage their own applications
  - Secure authentication and authorization

- **Modern UI**
  - Clean, responsive design
  - Bootstrap-based interface
  - Card and table views for applications
  - Status badges with color coding

## Project Structure

```
job-application-tracker/
├── app/                        # Main application package
│   ├── __init__.py             # Application factory
│   ├── auth/                   # Authentication module
│   │   ├── __init__.py
│   │   ├── forms.py            # Authentication forms
│   │   └── routes.py           # Authentication routes
│   ├── core/                   # Core module
│   │   ├── __init__.py
│   │   ├── db.py               # Database functions
│   │   ├── models.py           # Data models
│   │   ├── routes.py           # Core routes
│   │   └── schema.sql          # Database schema
│   ├── job_tracker/            # Job tracker module
│   │   ├── __init__.py
│   │   └── routes.py           # Job tracker routes
│   ├── static/                 # Static assets
│   │   ├── css/
│   │   │   ├── styles.css      # Global styles
│   │   │   └── job_tracker.css # Job tracker specific styles
│   │   └── js/
│   │       ├── main.js         # Global JavaScript
│   │       └── job_tracker.js  # Job tracker specific JavaScript
│   └── templates/              # HTML templates
│       ├── auth/               # Authentication templates
│       │   ├── login.html
│       │   ├── profile.html
│       │   └── register.html
│       ├── core/               # Core templates
│       │   └── index.html
│       ├── job_tracker/        # Job tracker templates
│       │   └── index.html
│       └── base.html           # Base template
├── instance/                   # Instance-specific data
│   └── job_tracker.db          # SQLite database
├── migrations/                 # Database migrations
│   └── migrate_data.py         # Data migration script
├── utils/                      # Utility scripts
│   └── setup.py                # Setup script
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows run script
├── run.sh                      # Unix run script
├── setup.bat                   # Windows setup script
├── setup.sh                    # Unix setup script
└── wsgi.py                     # WSGI entry point
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd job-application-tracker
   ```

2. **Run the setup script**

   On Windows:
   ```bash
   setup.bat
   ```

   On macOS/Linux:
   ```bash
   bash setup.sh
   ```

   This will:
   - Create a virtual environment
   - Install dependencies
   - Initialize the database
   - Migrate data from the old database (if it exists)

3. **Run the application**

   On Windows:
   ```bash
   run.bat
   ```

   On macOS/Linux:
   ```bash
   bash run.sh
   ```

4. **Access the application**

   Open your browser and navigate to `http://127.0.0.1:5000/`

5. **Default login credentials**

   - Email: demo@example.com
   - Password: password

## Adding New Projects to the Platform

The application is designed to be modular, making it easy to add new projects:

1. **Create a new module**

   Create a new directory in the `app` directory with the following files:
   - `__init__.py`: Blueprint initialization
   - `routes.py`: Routes for the new module

2. **Create templates**

   Create a new directory in the `app/templates` directory for your module's templates

3. **Register the blueprint**

   In `app/__init__.py`, import and register your new blueprint

4. **Add to the homepage**

   Add a new project card to the `app/templates/core/index.html` template

## Deployment

### Local Development

For local development, follow the setup and installation steps above.

### Production Deployment

For production deployment, additional steps are recommended:

1. **Set up a production server**

   - Use a production WSGI server like Gunicorn
   - Set up a reverse proxy with Nginx or Apache

2. **Configure environment variables**

   - Set `FLASK_ENV=production`
   - Set `FLASK_DEBUG=0`
   - Generate a strong `SECRET_KEY`

3. **Set up database backups**

   - Implement regular database backups
   - Consider using a more robust database for production

## License

[MIT License](LICENSE)
