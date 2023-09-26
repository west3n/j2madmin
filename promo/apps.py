from django.apps import AppConfig


class PromoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promo'
    verbose_name = "Аккаунты-Промо"

    def ready(self):
        import promo.signals
