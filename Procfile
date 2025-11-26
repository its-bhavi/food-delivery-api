release: python manage.py migrate --noinput && python create_test_user.py
web: gunicorn food_delivery_api.wsgi:application --bind 0.0.0.0:$PORT
