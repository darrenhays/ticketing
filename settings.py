from secrets.secrets import get_secret

SALT = get_secret('SALT').get('staging')
