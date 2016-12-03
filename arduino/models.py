# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from client.models import Client, Project as ProjectC
import uuid

from channels import Channel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict


def sensortype_files_name(instance, filename):
    today = timezone.now()
    today_path = today.strftime('%Y/%m/%d')
    return '/'.join(['sensor_type',
                     today_path,
                     'sensor_' + instance.name + '_' + str(instance.id),
                     filename])


class SensorType(models.Model):
    BOOLEAN = 0
    DECIMAL = 1
    INTEGER = 2
    STRING = 3

    DATA_TYPE_CHOICES = (
        (BOOLEAN, 'Booleano'),
        (DECIMAL, 'Decimal'),
        (INTEGER, 'Entero'),
        (STRING, 'Texto')
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=255,
        default=''
    )
    prefix = models.CharField(
        verbose_name='Prefijo',
        max_length=2,
        unique=True,
        default=''
    )
    subfix = models.CharField(
        verbose_name='Sufijo',
        max_length=2,
        blank=True,
        null=True
    )
    description = models.CharField(
        verbose_name='Descripción',
        max_length=255,
        default=''
    )
    model = models.CharField(
        verbose_name='Modelo de sensor',
        max_length=255,
        default=''
    )
    data_type = models.PositiveSmallIntegerField(
        choices=DATA_TYPE_CHOICES, default=1)
    data_sheet = models.FileField(
        verbose_name='Ficha técnica',
        upload_to=sensortype_files_name,
        blank=True,
        null=True
    )
    data_image = models.FileField(
        verbose_name='Imagen del sensor',
        upload_to=sensortype_files_name,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name + ': ' + self.description


class Arduino(models.Model):
    ESTATUS_CHOICES = (
        (1, 'Diseño'),
        (2, 'Construcción'),
        (3, 'Implementación'),
        (4, 'Mantenimiento/Pruebas'),
        (5, 'Producción'),
        (6, 'Fallo de Sistema')
    )

    project = models.ForeignKey(ProjectC, related_name="arduinos")
    name = models.CharField(max_length=255)
    arduino_token = models.CharField(max_length=80, unique=True)
    location = models.CharField(max_length=255)
    sensors = models.ManyToManyField(SensorType, through='ArduinoSensor')
    available_sensors = models.SmallIntegerField(default=1)
    estatus = models.PositiveSmallIntegerField(verbose_name='Estatus', choices=ESTATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    correos_alertas = models.CharField(
        verbose_name='Correos para alertas',
        max_length=255,
        blank=True,
        null=True
    )
    # objects = ArduinoManager()

    def __unicode__(self):
        return 'ID Arduino: ' + self.arduino_token

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            token = str(uuid.uuid4().hex)
            if len(token) > 20:
                token = token[0:20]
            self.arduino_token = token
        # self.objects.filter(arduino_id=self.arduino_id)
        super(Arduino, self).save(force_insert, force_update, using, update_fields)


class SensorEquipment(models.Model):
    project = models.ForeignKey(
        ProjectC,
        related_name='equipments',
        related_query_name='equipments',
        on_delete=models.CASCADE,
    )
    equipment_name = models.CharField(
        verbose_name='Nombre Refrigerador',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_model = models.CharField(
        verbose_name='Modelo Refrigerador',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_brand = models.CharField(
        verbose_name='Marca Refrigerador',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_buydate = models.CharField(
        verbose_name='Fecha de Compra',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_serial = models.CharField(
        verbose_name='No. Serie',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_size = models.CharField(
        verbose_name='Medidas del equipo',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_comments = models.CharField(
        verbose_name='Comentarios del equipo',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_notes = models.CharField(
        verbose_name='Notas Adicionales',
        max_length=255,
        blank=True,
        null=True
    )


class ArduinoSensor(models.Model):
    arduino = models.ForeignKey(
        Arduino,
        related_name='arduino_sensors',
        # to_field='arduino_token',
        on_delete=models.CASCADE
    )
    sensor_type = models.ForeignKey(
        SensorType,
        on_delete=models.CASCADE
    )
    equipment = models.ForeignKey(
        SensorEquipment,
        related_name='sensors',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    description = models.CharField(max_length=255)
    index = models.PositiveSmallIntegerField()
    data_key = models.CharField(max_length=20)
    max_value = models.DecimalField(
        verbose_name='Valor máximo permitido',
        max_digits=8,
        decimal_places=4,
        blank=True,
        null=True
    )
    min_value = models.DecimalField(
        verbose_name='Valor mínimo permitido',
        max_digits=8,
        decimal_places=4,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        # return str(self.id)
        # return 'Sensor: {0} Tipo:({1})'.format( self.sensor_type.name,
        return '{0} '.format(
            self.description,
        )


class SensorData(models.Model):
    arduino_sensor = models.ForeignKey(
        ArduinoSensor,
        related_name='sensor_data',
        related_query_name='sensor_data',
        on_delete=models.CASCADE,
    )
    data = models.CharField(max_length=255)
    epoch = models.PositiveIntegerField(default=0, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        get_latest_by = "epoch"

    def is_out_of_range(self):
        if self.data == '-127.00':
            return False

        if self.arduino_sensor.max_value < Decimal(self.data) \
                or self.arduino_sensor.min_value > Decimal(self.data):
            print('data out of range:', self.data)
            return True

        return False


# Se necesita guardar a que users se le envio?
class ArduinoAlert(models.Model):
    arduino = models.ForeignKey(Arduino, on_delete=models.CASCADE, related_name='alerts')
    # sensor = models.ForeignKey(ArduinoSensor, on_delete=models.CASCADE, related_name='alerts')
    sensors_in_alert = models.ManyToManyField(ArduinoSensor)
    sensor_data = models.ManyToManyField(SensorData)
    email_sends = models.ManyToManyField('EmailSend')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)

    def alert_action(self):

        try:
            latest_email_send = self.email_sends.latest()
        except EmailSend.DoesNotExist:
            latest_email_send = None

        delta = timezone.now() - timedelta(minutes=5)
        if False and (not latest_email_send or latest_email_send.sended_at <= delta):
            text_content = get_template('utils/email/alerta_rango.txt') \
                .render({'arduinoalert': self})
            html_content = get_template('utils/email/alerta_rango.html') \
                .render({'arduinoalert': self})
            email = EmailSend(
                from_email='alertas@esensait.com',
                to='joseangel.epzarce@gmail.com',
                subject='Hola',
                text_content=text_content,
                html_content=html_content,
            )
            email.save()
            email.send()
            self.email_sends.add(email)


class EmailSend(models.Model):
    from_email = models.CharField(max_length=510)
    to = models.CharField(max_length=510)
    subject = models.CharField(max_length=55)
    text_content = models.TextField()
    html_content = models.TextField()

    sended_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "sended_at"

    def send(self):
        # msg = EmailMultiAlternatives(
        #     self.subject,
        #     self.text_content,
        #     self.from_email,
        #     [self.to])
        # msg.attach_alternative(self.html_content, "text/html")
       # msg.send()

        self_dict = model_to_dict(self)
        Channel("send-email").send({
            "email_send": self_dict
        })


def merge_epoch_field(arduino, efield_name='field1'):
    sensors = arduino.arduino_sensors.all()
    esensor = sensors.filter(data_key=efield_name)
    delta = timedelta(seconds=3)
    for edata in esensor[0].sensor_data.all():
        edatetime = edata.created_at
        epoch = int(edata.data) + 180000
        SensorData.objects.filter(
            arduino_sensor__in=sensors,
            created_at__gt=edatetime - delta,
            created_at__lt=edatetime + delta
        ).update(epoch=epoch)


# @receiver(post_save, sender=SensorData)
# def post_save_sensordata(sender, instance, **kwargs):
#     instance_dict = model_to_dict(instance)
#     Channel("post-save-sensordata").send({
#         "sensordata": instance_dict
#     })
