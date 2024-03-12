from django.apps import AppConfig

class EcotrackAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecotrack_app'

    def ready(self):
        import ecotrack_app.signals
