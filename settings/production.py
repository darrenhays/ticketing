from secrets.secrets import get_secret


BASE_URL = 'https://puxbeuecqd.execute-api.us-east-2.amazonaws.com/production'
EVENTS_TABLE_NAME = 'events_production'
PURCHASES_TABLE_NAME = 'purchases_production'
SALT = get_secret('SECRETS').get('production_salt')
SESSIONS_TABLE_NAME = 'sessions_production'
TICKETS_TABLE_NAME = 'tickets_production'
TICKET_TYPES_TABLE_NAME = 'ticket_types_production'
USERS_TABLE_NAME = 'users_production'
