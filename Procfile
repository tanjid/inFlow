release: python manage.py migrate
web: gunicorn _keenthemes.wsgi
worker: python manage.py qcluster