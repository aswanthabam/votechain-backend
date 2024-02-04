# myapp/apps.py
from django.apps import AppConfig
from django.conf import settings
if not settings.DEBUG:
    from utils.face import FaceVerifier
class FaceConfig(AppConfig):
    name = 'api'
    def ready(self):
        if not settings.DEBUG:
            FaceVerifier()


