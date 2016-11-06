import os
import gevent.socket
import redis.connection


os.environ.update(DJANGO_SETTINGS_MODULE='ardsensor.settings')
from ws4redis.uwsgi_runserver import uWSGIWebsocketServer


redis.connection.socket = gevent.socket
application = uWSGIWebsocketServer()
