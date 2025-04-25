# tu_app/apps.py
from django.apps import AppConfig

class UfcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ufc'

    def ready(self):
        # Importa las señales cuando la app esté lista
        import ufc.signals  
