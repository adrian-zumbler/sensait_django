# In consumers.py
from channels import Channel, Group
from channels.sessions import channel_session


# Connected to chat-messages
def state_consumer(message):
    # Save to model
    arduino_token = message.content['arduino_token']
    # ChatMessage.objects.create(
    #     room=room,
    #     message=message.content['message'],
    # )
    # Broadcast to listening sockets
    Group("arduino-%s" % arduino_token).send({
        "text": message.content['state'],
    })

# Connected to websocket.connect
@channel_session
def ws_connect(message, arduino_token):
    # Work out room name from path (ignore slashes)
    # arduino_token = message.content['path'].strip("/")
    # Save room in session and add us to the group
    message.channel_session['arduino_token'] = arduino_token
    Group("arduino-%s" % arduino_token).add(message.reply_channel)

# Connected to websocket.receive
# @channel_session
# def ws_message(message):
#     # Stick the message onto the processing queue
#     Channel("arduino-messages").send({
#         "arduino_id": message.channel_session['arduino_id'],
#         "message": message['text'],
#     })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("arduino-%s" % message.channel_session['arduino_id']).discard(message.reply_channel)