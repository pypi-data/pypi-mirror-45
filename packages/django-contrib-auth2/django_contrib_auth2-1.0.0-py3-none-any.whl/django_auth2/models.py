from collections import namedtuple
from importlib import import_module

from .conf import get_setting

UserInfo = namedtuple('UserInfo', (
    'id',
    'email',
    'first_name',
    'last_name',
    'photo',
))


class InvalidProviderAccessToken(RuntimeError):
    pass


class InvalidRefreshToken(RuntimeError):
    pass


def get_provider_method(provider, method):
    providers = get_setting('AUTH2_PROVIDERS')

    for name, module in providers:
        if name == provider:
            provider = import_module(module)
            return getattr(provider, method)

    raise RuntimeError('Specified provider not installed.')


def get_oauth_userinfo(provider, credentials):
    return get_provider_method(provider, 'get_oauth_userinfo')(credentials)
