from secrets.secrets import get_secret

SALT = get_secret('SALT').get('staging')
CACHE_HOST = 'localhost'
CACHE_PORT = 6379
