import os
from secrets.secrets import get_secret


if os.environ.get('environment') == 'production':
    from settings.production import CACHE_HOST, CACHE_PORT, SALT_KEY, USERS_TABLE_NAME
else:
    from settings.staging import CACHE_HOST, CACHE_PORT, SALT_KEY, USERS_TABLE_NAME

SALT = get_secret('SALT').get(SALT_KEY)
