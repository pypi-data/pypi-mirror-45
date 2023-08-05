AUTH2_PROVIDERS = [
    ('google', 'django_auth2.providers.google'),
    ('facebook', 'django_auth2.providers.facebook'),
]

AUTH2_REFRESH_TOKEN_LIFETIME = 30 * 86400
AUTH2_REFRESH_TOKEN_MAX_LIFETIME = 365 * 86400
AUTH2_REFRESH_TOKEN_REGENERATE_THRESHOLD = 3 * 86400

AUTH2_CACHE_NAME = 'default'
AUTH2_CACHE_KEY = 'refresh_token:%s'
