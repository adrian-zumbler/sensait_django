# In consumers.py
from channels import Channel, Group
from arduino.models import SensorAlert
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from channels.sessions import channel_session, enforce_ordering


def post_save_sensordata(message):
    data = message.content['sensordata']
    sensor = data.arduino_sensor
    if data.is_in_alert():
        sensor_alert = SensorAlert.objects.get_or_create(
            arduino=sensor.arduino,
            sensor=sensor,
            active=True
        )
        sensor_alert.sensor_data.add(data)
        sensor_alert.alert_action(data)
    else:
        SensorAlert.objects.filter(
            arduino=sensor.arduino,
            sensor=sensor,
            active=True
        ).update(active=False, finished_at=timezone.now())


def send_email(message):
    emailsend = message.content['email_send']

    msg = EmailMultiAlternatives(
        emailsend['subject'],
        emailsend['text_content'],
        emailsend['from_email'],
        [emailsend['to']])
    msg.attach_alternative(emailsend['html_content'], "text/html")
    msg.send()


def state_consumer(message):

    arduino_token = message.content['arduino_token']

    state = message.content['state']
    try:
        Group("arduino-%s" % arduino_token).send({
            "text": state,
        })
    except Exception as e:
        raise e


# @channel_session
def ws_connect(message, arduino_token):
    Group("arduino-%s" % arduino_token).add(message.reply_channel)


def ws_keepalive(message, arduino_token):
    Group("arduino-%s" % arduino_token).add(message.reply_channel)


# @channel_session
def ws_disconnect(message, arduino_token):
    try:
        Group("arduino-%s" % arduino_token).discard(message.reply_channel)
    except Exception as e:
        print(e)