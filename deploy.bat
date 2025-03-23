@echo off
REM Production deployment script for Job Application Tracker on Windows
REM This script helps set up the application for production use with IIS

echo Job Application Tracker - Production Deployment (Windows)
echo ======================================================

REM Check for administrative privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Please run this script as Administrator
    exit /b 1
)

REM Get script directory
set SCRIPT_DIR=%~dp0
cd %SCRIPT_DIR%

REM Prompt for configuration
set /p DOMAIN_NAME=Enter the domain name for your application (e.g., tracker.example.com): 
set /p SECRET_KEY=Enter a strong secret key for Flask: 

REM Check for Python installation
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    exit /b 1
)

REM Set up Python environment
echo Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
pip install waitress

REM Create production .env file
echo Creating production .env file...
(
echo # Flask configuration
echo FLASK_APP=wsgi.py
echo FLASK_ENV=production
echo FLASK_DEBUG=0
echo.
echo # Application configuration
echo SECRET_KEY=%SECRET_KEY%
echo DATABASE_PATH=instance/job_tracker.db
echo.
echo # Server configuration
echo HOST=0.0.0.0
echo PORT=8000
) > .env

REM Create Windows service using NSSM (Non-Sucking Service Manager)
echo Downloading NSSM...
powershell -Command "Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'"
powershell -Command "Expand-Archive -Path 'nssm.zip' -DestinationPath 'nssm' -Force"

echo Installing Job Tracker as a Windows service...
if exist %PROCESSOR_ARCHITECTURE:~-2% == 64 (
    set NSSM_EXE=nssm\nssm-2.24\win64\nssm.exe
) else (
    set NSSM_EXE=nssm\nssm-2.24\win32\nssm.exe
)

%NSSM_EXE% install JobTracker "%SCRIPT_DIR%venv\Scripts\waitress-serve.exe"
%NSSM_EXE% set JobTracker AppParameters "--host=0.0.0.0 --port=8000 wsgi:app"
%NSSM_EXE% set JobTracker AppDirectory "%SCRIPT_DIR%"
%NSSM_EXE% set JobTracker DisplayName "Job Application Tracker"
%NSSM_EXE% set JobTracker Description "Flask-based job application tracking web application"
%NSSM_EXE% set JobTracker Start SERVICE_AUTO_START
%NSSM_EXE% set JobTracker AppStdout "%SCRIPT_DIR%logs\service.log"
%NSSM_EXE% set JobTracker AppStderr "%SCRIPT_DIR%logs\service.log"

REM Create logs directory
mkdir logs

REM Start the service
echo Starting the Job Tracker service...
net start JobTracker

REM Create backup script
echo Creating database backup script...
(
echo @echo off
echo set BACKUP_DIR=%SCRIPT_DIR%backups
echo set TIMESTAMP=%%date:~-4%%%%date:~3,2%%%%date:~0,2%%_%%time:~0,2%%%%time:~3,2%%%%time:~6,2%%
echo set TIMESTAMP=%%TIMESTAMP: =0%%
echo mkdir "%%BACKUP_DIR%%" 2^>nul
echo copy "instance\job_tracker.db" "%%BACKUP_DIR%%\job_tracker_%%TIMESTAMP%%.db"
echo.
echo REM Keep only the 10 most recent backups
echo for /f "skip=10 delims=" %%%%i in ^('dir /b /o-d "%%BACKUP_DIR%%\job_tracker_*.db"'^) do del "%%BACKUP_DIR%%\%%%%i"
) > backup.bat

REM Create scheduled task for backups
echo Setting up daily database backups...
schtasks /create /tn "JobTrackerBackup" /tr "%SCRIPT_DIR%backup.bat" /sc daily /st 00:00 /ru SYSTEM /f

echo.
echo Deployment completed!
echo.
echo Next steps:
echo 1. Install Nginx Proxy Manager using Docker Desktop for Windows
echo    - Download and install Docker Desktop from https://www.docker.com/products/docker-desktop
echo    - Create a directory for Nginx Proxy Manager
echo    - Create a docker-compose.yml file with the following content:
echo.
echo      version: '3'
echo      services:
echo        app:
echo          image: 'jc21/nginx-proxy-manager:latest'
echo          restart: unless-stopped
echo          ports:
echo            - '80:80'
echo            - '81:81'
echo            - '443:443'
echo          volumes:
echo            - ./data:/data
echo            - ./letsencrypt:/etc/letsencrypt
echo.
echo    - Run 'docker-compose up -d' in that directory
echo.
echo 2. Access Nginx Proxy Manager at http://localhost:81
echo    - Default login: admin@example.com / changeme
echo.
echo 3. Add a proxy host for your application:
echo    - Domain: %DOMAIN_NAME%
echo    - Forward to: http://localhost:8000
echo    - Enable SSL with Let's Encrypt
echo.
echo Your Job Application Tracker will be available at https://%DOMAIN_NAME%
echo once you've completed the Nginx Proxy Manager configuration.
