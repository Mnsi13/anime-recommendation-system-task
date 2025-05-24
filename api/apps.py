# from django.apps import AppConfig


# class ApiConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'api'
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Only run this on Render (production), not on migrations or tests
        import os
        if os.environ.get("RENDER", "False") == "True":
            try:
                from . import create_superuser
            except Exception as e:
                print(f"Superuser creation failed: {e}")
