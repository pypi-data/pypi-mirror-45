from random import randint

from django.conf import settings
from django.core.cache import caches
from django.utils.timezone import now

from .conf import get_setting
from .models import InvalidRefreshToken
from .utils import sha256, retry


@retry(max_retries=10)
def create_refresh_token(user_id, device_id):
    cache_name = get_setting('AUTH2_CACHE_NAME')
    cache_key = get_setting('AUTH2_CACHE_KEY')
    token_lifetime = get_setting('AUTH2_REFRESH_TOKEN_LIFETIME')
    token_max_lifetime = get_setting('AUTH2_REFRESH_TOKEN_MAX_LIFETIME')

    cache = caches[cache_name]
    refresh_token = sha256(''.join((
        str(settings.SECRET_KEY),
        str(user_id),
        str(device_id),
        str(now().timestamp()),
        str(randint(1000000, 9999999))
    )))

    expire_at = int(now().timestamp()) + token_max_lifetime

    data = {
        'user_id': user_id,
        'device_id': device_id,
        'expire_at': expire_at
    }

    if not cache.add(cache_key % refresh_token, data, token_lifetime):
        raise RuntimeError('Cannot create new refresh token')

    return refresh_token


def extend_refresh_token(refresh_token):
    cache_name = get_setting('AUTH2_CACHE_NAME')
    cache_key = get_setting('AUTH2_CACHE_KEY')
    regenerate_threshold = get_setting(
        'AUTH2_REFRESH_TOKEN_REGENERATE_THRESHOLD'
    )

    cache = caches[cache_name]

    token_data = cache.get(cache_key % refresh_token)

    if token_data['expire_at'] - int(now().timestamp()) < regenerate_threshold:
        device = load_refresh_token(refresh_token)
        new_refresh_token = create_refresh_token(device)
        return new_refresh_token

    return refresh_token


def load_refresh_token(refresh_token, expected_device_id=None):
    cache_name = get_setting('AUTH2_CACHE_NAME')
    cache_key = get_setting('AUTH2_CACHE_KEY')
    token_lifetime = get_setting('AUTH2_REFRESH_TOKEN_LIFETIME')

    cache = caches[cache_name]

    data = cache.get(cache_key % refresh_token)
    if not data:
        raise InvalidRefreshToken()

    if expected_device_id and expected_device_id != data['device_id']:
        raise InvalidRefreshToken()

    cache.touch(cache_key % refresh_token, token_lifetime)

    return data['user_id'], data['device_id']
