from django.apps import AppConfig


class AppWebgendaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_webgenda'

    def ready(self):
            import app_webgenda.signals