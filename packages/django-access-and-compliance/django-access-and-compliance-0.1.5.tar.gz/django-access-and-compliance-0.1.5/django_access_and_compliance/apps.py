from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in

from .config import access_and_compliance_group_name


class AccessAndComplianceConfig(AppConfig):
    name = 'django_access_and_compliance'
    verbose = 'Access and Compliance'

    def ready(self):
        from .signals import ensure_compliant
        user_logged_in.connect(ensure_compliant)
