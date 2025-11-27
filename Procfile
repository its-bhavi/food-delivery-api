release: python check_database.py && python manage.py migrate --noinput && python create_test_user.py && python create_admin.py
web: gunicorn food_delivery_api.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
