from django.apps import AppConfig


class MulimaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mulima_app'

    def ready(self):
        import mulima_app.signals