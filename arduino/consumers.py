# In consumers.py
import json
from channels import Channel, Group
from arduino.models import ArduinoAlert
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from channels.sessions import channel_session, enforce_ordering

from io import BytesIO

from django.utils import timezone
from django.core.files import File
from ardsensor.printing import ReportPrint

from arduino.models import SensorData, Report


def post_save_sensordata(message):
    data = message.content['sensordata']
    data = SensorData.objects.get(id=data['id'])
    sensor = data.arduino_sensor
    if data.is_out_of_range():
        arduino_alert, created = ArduinoAlert.objects.get_or_create(
            arduino=sensor.arduino,
            # sensor=sensor,
            active=True
        )
        if sensor not in arduino_alert.sensors_in_alert.all():
                arduino_alert.sensors_in_alert.add(sensor)
        arduino_alert.sensor_data.add(data)
        arduino_alert.alert_action(data)
    else:
        arduino_alerts = sensor.arduino.alerts.filter(active=True)
        for alert in arduino_alerts:
            if sensor in alert.sensors_in_alert.all():
                alert.sensors_in_alert.remove(sensor)
            if not alert.sensors_in_alert.all().exists():
                alert.active = False
                alert.finished_at = timezone.now()
                alert.save()


def create_file(message):
    instance = Report.objects.get(
        id=message.content['instance_id']
    ).create_update_file()
    instance._signal_sended = True
    instance.save()


def arduino_alert(message):
    data_list = [SensorData.objects.get(id=data['id'])
                 for data in json.loads(message.content['data_list'])]
    arduino = data_list[0].arduino_sensor.arduino
    arduino_active_alerts = arduino.alerts.filter(active=True)
    for data in data_list:
        sensor = data.arduino_sensor
        if data.is_out_of_range():
            arduino_alert, created = ArduinoAlert.objects.get_or_create(
                arduino=sensor.arduino,
                active=True
            )
            if sensor not in arduino_alert.sensors_in_alert.all():
                    arduino_alert.sensors_in_alert.add(sensor)
            arduino_alert.sensor_data.add(data)
        else:
            for alert in arduino_active_alerts:
                if sensor in alert.sensors_in_alert.all():
                    alert.sensors_in_alert.remove(sensor)
                if not alert.sensors_in_alert.all().exists():
                    alert.active = False
                    alert.finished_at = timezone.now()
                    alert.save()

    # Si quedan alertas activas ejecuta accion
    try:
        arduino_active_alerts.latest(
            field_name='created_at'
        ).alert_action()
    except Exception as e:
        pass


def send_email(message):
    emailsend = message.content['email_send']

    msg = EmailMultiAlternatives(
        emailsend['subject'],
        emailsend['text_content'],
        emailsend['from_email'],
        emailsend['to'].split(","))
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