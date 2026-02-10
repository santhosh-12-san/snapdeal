import os
from django.core.wsgi import get_wsgi_application

# CHANGED: 'snapdeal_clone.settings' -> 'config.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()