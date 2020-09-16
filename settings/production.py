import stripe
from secrets.secrets import get_secret


BASE_URL = 'https://puxbeuecqd.execute-api.us-east-2.amazonaws.com/production'
EVENTS_TABLE_NAME = 'events_production'
PURCHASES_TABLE_NAME = 'purchases_production'
SALT = get_secret('SECRETS').get('production_salt')
SESSIONS_TABLE_NAME = 'sessions_production'
TICKETS_TABLE_NAME = 'tickets_production'
TICKET_TYPES_TABLE_NAME = 'ticket_types_production'
USERS_TABLE_NAME = 'users_production'
STRIPE_SECRET_API_KEY = get_secret('SECRETS').get('stripe_api_key')
STRIPE_PUBLIC_API_KEY = "pk_test_51HPtHoCZ4yfyFkHo8VsiFZtp5vbuCsRyD7qLTlUf1Gqp5PwmmE4xnBTc7QlwwBOnm4Wp0y2HIcVi6316eLUp5QrF00BNgrSrBN"
stripe.api_key = STRIPE_SECRET_API_KEY
