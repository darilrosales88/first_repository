from django.apps import AppConfig


class NomencladoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nomencladores'

    def ready(self):
        import nomencladores.signals  # Importar las señales
