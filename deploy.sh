#!/bin/bash

# Production deployment script for Job Application Tracker
# This script helps set up the application for production use

echo "Job Application Tracker - Production Deployment"
echo "=============================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script with sudo or as root"
  exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Prompt for configuration
read -p "Enter the username to run the service as: " SERVICE_USER
read -p "Enter the domain name for your application (e.g., tracker.example.com): " DOMAIN_NAME
read -p "Enter your email address (for SSL certificate): " EMAIL_ADDRESS
read -s -p "Enter a strong secret key for Flask: " SECRET_KEY
echo ""

# Install required packages
echo "Installing required system packages..."
apt-get update
apt-get install -y python3 python3-venv python3-pip docker.io docker-compose

# Set up Python environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Create production .env file
echo "Creating production .env file..."
cat > .env << EOF
# Flask configuration
FLASK_APP=wsgi.py
FLASK_ENV=production
FLASK_DEBUG=0

# Application configuration
SECRET_KEY=$SECRET_KEY
DATABASE_PATH=instance/job_tracker.db

# Server configuration
HOST=0.0.0.0
PORT=8000
EOF

# Create systemd service file
echo "Creating systemd service file..."
cat > /etc/systemd/system/job-tracker.service << EOF
[Unit]
Description=Job Application Tracker
After=network.target

[Service]
User=$SERVICE_USER
WorkingDirectory=$SCRIPT_DIR
Environment="PATH=$SCRIPT_DIR/venv/bin"
ExecStart=$SCRIPT_DIR/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Set up Nginx Proxy Manager
echo "Setting up Nginx Proxy Manager..."
mkdir -p /opt/nginx-proxy-manager
cd /opt/nginx-proxy-manager

cat > docker-compose.yml << EOF
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

docker-compose up -d

# Create backup script
echo "Creating database backup script..."
cd "$SCRIPT_DIR"
cat > backup.sh << EOF
#!/bin/bash
BACKUP_DIR="$SCRIPT_DIR/backups"
TIMESTAMP=\$(date +"%Y%m%d_%H%M%S")
mkdir -p "\$BACKUP_DIR"
cp instance/job_tracker.db "\$BACKUP_DIR/job_tracker_\$TIMESTAMP.db"
# Keep only the 10 most recent backups
ls -t "\$BACKUP_DIR"/job_tracker_*.db | tail -n +11 | xargs -r rm
EOF

chmod +x backup.sh

# Set up cron job for backups
echo "Setting up daily database backups..."
(crontab -l 2>/dev/null; echo "0 0 * * * $SCRIPT_DIR/backup.sh") | crontab -

# Enable and start the service
echo "Enabling and starting the Job Tracker service..."
systemctl enable job-tracker
systemctl start job-tracker

echo ""
echo "Deployment completed!"
echo ""
echo "Next steps:"
echo "1. Access Nginx Proxy Manager at http://your-server-ip:81"
echo "   - Default login: admin@example.com / changeme"
echo "2. Add a proxy host for your application:"
echo "   - Domain: $DOMAIN_NAME"
echo "   - Forward to: http://localhost:8000"
echo "   - Enable SSL with Let's Encrypt using email: $EMAIL_ADDRESS"
echo ""
echo "Your Job Application Tracker will be available at https://$DOMAIN_NAME"
echo "once you've completed the Nginx Proxy Manager configuration."
