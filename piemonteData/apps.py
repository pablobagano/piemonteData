from django.apps import AppConfig


class PiemontedataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "piemonteData"
    
    def ready(self):
        import piemonteData.signals