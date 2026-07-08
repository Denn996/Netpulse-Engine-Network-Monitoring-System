from django.apps import AppConfig


class NetpulseEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Netpulse_Engine'


    def ready(self):
       import Netpulse_Engine.signals
