import os


environment = os.environ.get('environment')

if environment == 'production':
    from settings.production import *
elif environment == 'staging':
    from settings.staging import *
else:
    from settings.local import *
