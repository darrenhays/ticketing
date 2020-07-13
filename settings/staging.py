from secrets.secrets import get_secret


BASE_URL = 'https://kg3bhyded2.execute-api.us-east-2.amazonaws.com/staging'
SALT = get_secret('SALT').get('staging')
SESSIONS_TABLE_NAME = "sessions_staging"
USERS_TABLE_NAME = "users_staging"
