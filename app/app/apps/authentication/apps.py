from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.apps.authentication'

    def ready(self) -> None:
        import app.apps.authentication.signals
        return super().ready()
