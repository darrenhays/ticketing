from secrets.secrets import get_secret


BASE_URL = 'https://puxbeuecqd.execute-api.us-east-2.amazonaws.com/production'
SALT = get_secret('SALT').get('production')
SESSIONS_TABLE_NAME = "sessions_production"
USERS_TABLE_NAME = "users_production"
