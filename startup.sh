#!/bin/sh

echo ""
echo "Kedawan! A simple URL shortener."
echo ""


# Perform the database migration
echo "Performing database migration (upgrade)..."
flask db upgrade


# Run Gunicorn and bind it to 0.0.0.0
echo "Starting app..."
gunicorn --bind 0.0.0.0:8000 app:app
