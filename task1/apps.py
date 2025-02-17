from django.apps import AppConfig


class Task1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task1'


    def ready(self):
        import task1.signals
