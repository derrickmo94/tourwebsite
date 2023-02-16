from django.apps import AppConfig


class TourConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tour'

    def ready(self):
        import apps.tour.signals
