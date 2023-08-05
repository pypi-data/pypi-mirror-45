import requests
import logging

from django.conf import settings
from django.contrib.auth.models import Group

from .config import access_and_compliance_group_name

logger = logging.getLogger(__name__)


def ensure_compliant(sender, request, user, **kwargs):
    payload = {'uniqname': user.username}
    response = requests.get(settings.ACCESS_AND_COMPLIANCE_VALIDATION_URL, params=payload)
    response.raise_for_status()
    group, created = Group.objects.get_or_create(name=access_and_compliance_group_name)

    if _is_compliant(response):
        group.user_set.add(user)
        logger.debug(f'{user} has attested to the data access and compliance policy')
    else:
        group.user_set.remove(user)
        logger.debug(f'{user} has not attested to data compliance policy')


def _is_compliant(response):
    return response.text in settings.ACCESS_AND_COMPLIANCE_TRUTHY_VALUES
