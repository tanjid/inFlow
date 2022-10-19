from django.apps import AppConfig


class ResellerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reseller'


    def ready(self):
        import reseller.signals