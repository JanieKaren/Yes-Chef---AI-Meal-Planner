"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Set the Django settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Get the Django WSGI application
django_application = get_wsgi_application()

# Wrap with WhiteNoise
application = WhiteNoise(
    django_application,
    root=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles'),
    prefix='static/'
)