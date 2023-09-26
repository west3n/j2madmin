from django.apps import AppConfig


class WeeklyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weekly'
    verbose_name = 'Расчет недельного баланса'

    def ready(self):
        from weekly import signals
