#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your project
python -m pip install --upgrade pip

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
