release: python manage.py migrate --noinput
web: gunicorn food_delivery_api.wsgi:application --bind 0.0.0.0:$PORT
