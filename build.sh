#!/usr/bin/env bash
# exit on error
set -o errexit

echo "===> Installing dependencies..."
pip install -r requirements.txt

echo "===> Collecting static files..."
python manage.py collectstatic --no-input

echo "===> Running migrations..."
python manage.py migrate

echo "===> Creating superuser if needed..."
# Check if CREATE_SUPERUSER environment variable is set
if [[ -n "$CREATE_SUPERUSER" ]]; then
    echo "Creating superuser with username: $DJANGO_SUPERUSER_USERNAME"
    python manage.py createsuperuser --noinput || true
    echo "Superuser creation complete!"
else
    echo "Skipping superuser creation (CREATE_SUPERUSER not set)"
fi

echo "===> Build complete!"
