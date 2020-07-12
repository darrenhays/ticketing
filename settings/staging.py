from secrets.secrets import get_secret


CACHE_HOST = 'localhost'
CACHE_PORT = 6379
USERS_TABLE_NAME = "users_staging"
SALT = get_secret('SALT').get('staging')
