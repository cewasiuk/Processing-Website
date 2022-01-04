from django.apps import AppConfig


class InProcessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'in_process'
