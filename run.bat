@echo off
echo Starting Job Application Tracker...

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting Flask server...
flask --app wsgi.py run

pause
