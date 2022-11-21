echo "is_testing = False" > config.py
gunicorn --bind 0.0.0.0:5000 wsgi:app
