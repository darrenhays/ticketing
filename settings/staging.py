from secrets.secrets import get_secret


BASE_URL = 'https://kg3bhyded2.execute-api.us-east-2.amazonaws.com/staging'
EVENTS_TABLE_NAME = 'events_staging'
PURCHASES_TABLE_NAME = 'purchases_staging'
SALT = get_secret('SECRETS').get('staging_salt')
SESSIONS_TABLE_NAME = 'sessions_staging'
TICKETS_TABLE_NAME = 'tickets_staging'
TICKET_TYPES_TABLE_NAME = 'ticket_types_staging'
USERS_TABLE_NAME = 'users_staging'
