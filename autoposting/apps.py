from django.apps import AppConfig


class AutopostingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoposting'
    verbose_name = 'Панель автопостинга'

    def ready(self):
        import autoposting.signals
