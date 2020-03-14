release: python manage.py migrate
worker: celery -A app worker -B -l info
web: gunicorn app.wsgi