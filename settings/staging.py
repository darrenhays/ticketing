import stripe
from secrets.secrets import get_secret


BASE_URL = 'https://0dny54d3nf.execute-api.us-east-2.amazonaws.com/staging'
LAMBDA_URL = BASE_URL
EVENTS_TABLE_NAME = 'events_staging'
PROCESS_TABLE_NAME = 'processes_staging'
PURCHASES_TABLE_NAME = 'purchases_staging'
SALT = get_secret('SECRETS').get('staging_salt')
SESSIONS_TABLE_NAME = 'sessions_staging'
TICKETS_TABLE_NAME = 'tickets_staging'
TICKET_TYPES_TABLE_NAME = 'ticket_types_staging'
USERS_TABLE_NAME = 'users_staging'
STRIPE_SECRET_API_KEY = get_secret('SECRETS').get('stripe_api_key')
STRIPE_PUBLIC_API_KEY = "pk_test_51HPtHoCZ4yfyFkHo8VsiFZtp5vbuCsRyD7qLTlUf1Gqp5PwmmE4xnBTc7QlwwBOnm4Wp0y2HIcVi6316eLUp5QrF00BNgrSrBN"
stripe.api_key = STRIPE_SECRET_API_KEY
QUEUE_URL = 'https://sqs.us-east-2.amazonaws.com/531085525366/bulk_refund'
