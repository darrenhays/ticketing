import os


if os.environ.get('environment') == 'production':
    from settings.production import CACHE_HOST, CACHE_PORT, SALT, USERS_TABLE_NAME
else:
    from settings.staging import CACHE_HOST, CACHE_PORT, SALT, USERS_TABLE_NAME

