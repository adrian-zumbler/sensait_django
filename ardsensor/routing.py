from channels.routing import route
from arduino.consumers import ws_connect, ws_disconnect, state_consumer, send_email, post_save_sensordata

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/ws/arduino/(?P<arduino_token>[a-zA-Z0-9_]+)$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/ws/arduino/(?P<arduino_token>[a-zA-Z0-9_]+)$"),
    route("arduino-state", state_consumer),
    route('send-email', send_email),
    route('post-send-sensordata', post_save_sensordata)
]