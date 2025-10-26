#!/bin/bash
# Install packages in the virtual environment

# Activate virtual environment
source ../.venv/bin/activate

# Install packages
pip install -r requirements.txt

echo "Packages installed in virtual environment!"
echo "You can now run: python manage.py runserver"

