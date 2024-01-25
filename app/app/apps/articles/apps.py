from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.apps.articles'

    def ready(self) -> None:
        import app.apps.articles.signals
        
        return super().ready()