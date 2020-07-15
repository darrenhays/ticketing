from secrets.secrets import get_secret


BASE_URL = 'https://kg3bhyded2.execute-api.us-east-2.amazonaws.com/staging'
EVENTS_TABLE_NAME = 'events_staging'
SALT = get_secret('SALT').get('staging')
SESSIONS_TABLE_NAME = "sessions_staging"
TICKET_TYPES_TABLE_NAME = 'ticket_types_staging'
USERS_TABLE_NAME = "users_staging"
