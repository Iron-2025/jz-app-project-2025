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

For production deployment, we've provided automated deployment scripts for both Linux and Windows environments.

#### Using the Deployment Scripts

1. **Linux/macOS Deployment**

   Run the deployment script with sudo:

   ```bash
   sudo bash deploy.sh
   ```

   The script will:
   - Install required packages
   - Set up a Python virtual environment
   - Configure environment variables
   - Create a systemd service
   - Set up Nginx Proxy Manager with Docker
   - Configure database backups
   - Start the application

2. **Windows Deployment**

   Run the deployment script as Administrator:

   ```
   deploy.bat
   ```

   The script will:
   - Set up a Python virtual environment
   - Configure environment variables
   - Install the application as a Windows service using NSSM
   - Set up scheduled database backups
   - Provide instructions for setting up Nginx Proxy Manager with Docker Desktop

#### Manual Deployment

If you prefer to deploy manually, follow these steps:

1. **Set up a production server**

   - Install Python 3.8+ on your server
   - Clone the repository to your server
   - Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**

   Create a `.env` file in the project root with production settings:

   ```
   # Flask configuration
   FLASK_APP=wsgi.py
   FLASK_ENV=production
   FLASK_DEBUG=0

   # Application configuration
   SECRET_KEY=your-strong-secret-key-here  # Generate a strong random key
   DATABASE_PATH=instance/job_tracker.db

   # Server configuration
   HOST=0.0.0.0  # Listen on all interfaces
   PORT=8000     # Use a different port than development
   ```

3. **Set up a WSGI server**

   For Linux/macOS:
   ```bash
   pip install gunicorn
   gunicorn --workers 3 --bind 0.0.0.0:8000 wsgi:app
   ```

   For Windows:
   ```bash
   pip install waitress
   waitress-serve --host=0.0.0.0 --port=8000 wsgi:app
   ```

4. **Set up Nginx Proxy Manager**

   Nginx Proxy Manager provides an easy-to-use web interface for managing Nginx proxy hosts with SSL certificates.

   a. **Install Nginx Proxy Manager**

   The easiest way to install Nginx Proxy Manager is using Docker:

   ```bash
   # Create a directory for Nginx Proxy Manager
   mkdir -p /path/to/nginx-proxy-manager
   cd /path/to/nginx-proxy-manager

   # Create a docker-compose.yml file
   cat > docker-compose.yml << 'EOF'
   version: '3'
   services:
     app:
       image: 'jc21/nginx-proxy-manager:latest'
       restart: unless-stopped
       ports:
         - '80:80'
         - '81:81'
         - '443:443'
       volumes:
         - ./data:/data
         - ./letsencrypt:/etc/letsencrypt
   EOF

   # Start Nginx Proxy Manager
   docker-compose up -d
   ```

   b. **Access the Nginx Proxy Manager dashboard**

   - Open your browser and navigate to `http://your-server-ip:81`
   - Default login credentials:
     - Email: `admin@example.com`
     - Password: `changeme`
   - You'll be prompted to change these credentials on first login

   c. **Add a proxy host for your application**

   - In the dashboard, go to "Proxy Hosts" and click "Add Proxy Host"
   - Fill in the following details:
     - Domain Names: `your-domain.com` (the domain you want to use)
     - Scheme: `http`
     - Forward Hostname / IP: `localhost` (or your server's internal IP)
     - Forward Port: `8000` (the port your application is running on)
     - Check "Block Common Exploits"
   - In the SSL tab:
     - Check "Request a new SSL Certificate"
     - Check "Force SSL"
     - Check "HTTP/2 Support"
     - Email: Your email for Let's Encrypt notifications
   - Click "Save"

   Nginx Proxy Manager will automatically obtain an SSL certificate from Let's Encrypt and configure the proxy.

5. **Security considerations**

   - Ensure your server's firewall allows traffic only on ports 80, 443, and SSH
   - Set up fail2ban to protect against brute force attacks
   - Keep your system and packages updated regularly
   - Consider using a more robust database like PostgreSQL for production

## License

[MIT License](LICENSE)
