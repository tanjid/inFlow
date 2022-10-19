from django.apps import AppConfig


class MarketPlacePrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market_place_prder'


    def ready(self):
        import market_place_prder.signals