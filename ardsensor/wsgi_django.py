import os
from django.core.wsgi import get_wsgi_application

os.environ.update(DJANGO_SETTINGS_MODULE='ardsensor.settings')
application = get_wsgi_application()