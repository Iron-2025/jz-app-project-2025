#!/bin/bash

echo "Starting Job Application Tracker..."

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting Flask server..."
flask --app wsgi.py run
