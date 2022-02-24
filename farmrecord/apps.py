from django.apps import AppConfig


class FarmrecordConfig(AppConfig):
    name = 'farmrecord'

    def ready(self):
        from farmrecord import signals