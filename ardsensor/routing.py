from channels.routing import route
from arduino.consumers import ws_connect, ws_disconnect, state_consumer

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/ws/arduino/(?P<arduino_token>[a-zA-Z0-9_]+)$"),
    #route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
    route("arduino-state", state_consumer),
]