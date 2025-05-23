"""
WSGI config for anime_recommender project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
print("DEBUG: WSGI loaded")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime_recommender.settings')

application = get_wsgi_application()
