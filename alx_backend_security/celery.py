import os
from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_security.settings")

app = Celery("alx_backend_security")

# Load settings from Django settings.py using CELERY_ namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all registered apps
app.autodiscover_tasks()