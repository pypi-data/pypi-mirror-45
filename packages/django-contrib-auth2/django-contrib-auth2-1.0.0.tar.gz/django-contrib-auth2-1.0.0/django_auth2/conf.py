from django.conf import settings

from django_auth2 import default_settings


def get_setting(key):
    return getattr(settings, key, getattr(default_settings, key))
