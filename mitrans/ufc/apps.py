from django.apps import AppConfig


class UfcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ufc'

    def ready(self):
        pass  # Registrar señales, de esta manera las señales se ejecutarán 
