from secrets.secrets import get_secret


BASE_URL = 'https://puxbeuecqd.execute-api.us-east-2.amazonaws.com/production'
EVENTS_TABLE_NAME = 'events_production'
SALT = get_secret('SALT').get('production')
SESSIONS_TABLE_NAME = "sessions_production"
TICKET_TYPES_TABLE_NAME = 'ticket_types_production'
USERS_TABLE_NAME = "users_production"
