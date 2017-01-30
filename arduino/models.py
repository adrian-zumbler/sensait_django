# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from decimal import Decimal
from datetime import timedelta, datetime
from io import BytesIO

from django.utils import timezone
from django.core.files import File
from django.db import models
from django.contrib.auth.models import User
from django.template.loader import get_template

from client.models import Client, Project as ProjectC
from ardsensor.printing import ReportPrint
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
    name = models.CharField(max_length=255, verbose_name='Nombre del Transmisor')
    modelo_transmisor = models.CharField(
        verbose_name='Modelo del transmisor',
        max_length=255,
        blank=True,
        null=True
    )
    arduino_token = models.CharField(max_length=80, unique=True)
    location = models.CharField(max_length=255, verbose_name='Ubicación Fisica del Transmisor')
    sensors = models.ManyToManyField(SensorType, through='ArduinoSensor')
    available_sensors = models.SmallIntegerField(default=1)
    estatus = models.PositiveSmallIntegerField(verbose_name='Estatus', choices=ESTATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    correos_alertas = models.CharField(
        verbose_name='Correos para alertas (Separados por , )',
        max_length=255,
        blank=True,
        null=True
    )
    delta_time_alerts = models.PositiveSmallIntegerField(
        verbose_name='Tiempo entre envio de alertas',
        default=5
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
        verbose_name='Projecto Relacionado',
        on_delete=models.CASCADE,
    )
    equipment_name = models.CharField(
        verbose_name='Nombre Equipo',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_model = models.CharField(
        verbose_name='Modelo',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_brand = models.CharField(
        verbose_name='Marca',
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
        verbose_name='Número de Serie',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_size = models.CharField(
        verbose_name='Dimensiones Fisicas',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_capacity = models.CharField(
        verbose_name='Capacidad',
        max_length=50,
        blank=True,
        null=True
    )
    equipment_operativerange = models.CharField(
        verbose_name='Rango Operativo',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_exclusas = models.CharField(
        verbose_name='Exclusas',
        max_length=255,
        blank=True,
        null=True
    )
    equipment_comments = models.CharField(
        verbose_name='Sitio web del Equipo',
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

    def __unicode__(self):
        return self.equipment_name


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

        delta = timezone.now() - timedelta(minutes=self.arduino.delta_time_alerts)
        if self.arduino.correos_alertas \
                and (not latest_email_send or latest_email_send.sended_at <= delta):
            text_content = get_template('utils/email/alerta_rango.txt') \
                .render({'arduinoalert': self})
            html_content = get_template('utils/email/alerta_rango.html') \
                .render({'arduinoalert': self})
            email = EmailSend(
                from_email='alertas@sensait.com',
                to=self.arduino.correos_alertas,
                subject='Alerta Sensait - El equipo %s detectó una lectura fuera de rango. Folio: 000%s' % (self.arduino.name, self.id),
                text_content=text_content,
                html_content=html_content,
            )
            email.save()
            email.send()
            self.email_sends.add(email)

    def sensor_alerts(self):
        for sensor_alert in self.sensors_in_alert.all():
            sensor_alert.data = self.sensor_data.filter(
                arduino_sensor=sensor_alert
            )
            sensor_alert.finished_at = '---'
            yield sensor_alert

        for sensor_alert in self.sensor_safe_alerts():
            yield sensor_alert

    def sensor_safe_alerts(self):
        safe_data = self.sensor_data.exclude(
            arduino_sensor__in=self.sensors_in_alert.all()
        )
        while safe_data:
            sensor_safe_alert = safe_data[0].arduino_sensor
            sensor_safe_alert.data = safe_data.filter(
                arduino_sensor=sensor_safe_alert
            )

            sensor_safe_alert.finished_at = sensor_safe_alert.data.last().epoch

            safe_data = safe_data.exclude(
                arduino_sensor=sensor_safe_alert
            )
            yield sensor_safe_alert


class EmailSend(models.Model):
    from_email = models.CharField(max_length=510)
    to = models.CharField(max_length=510)
    subject = models.CharField(max_length=255)
    text_content = models.TextField()
    html_content = models.TextField()

    sended_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "sended_at"

    def send(self):
        self_dict = model_to_dict(self)
        Channel("send-email").send({
            "email_send": self_dict
        })


def report_files_name(instance, filename):
    today = timezone.now()
    today_path = today.strftime('%Y/%m/%d')
    return '/'.join([
        'report',
        today_path,
        str(instance.sensor.id),
        'Reporte' + '-' + datetime.fromtimestamp(instance.fecha_inicial).strftime('%d-%m-%Y') + '_' + datetime.fromtimestamp(instance.fecha_final).strftime('%d-%m-%Y') + '.pdf']
    )


class Report(models.Model):
    REPORTES_TIPO = (
        (1, 'Reporte de Registros'),
        (2, 'Reporte de Alertas')
    )

    ARCHIVO_TIPO = (
        (1, 'PDF'),
        (2, 'CSV'),
        (3, 'XLSX')
    )

    sensor = models.ForeignKey(ArduinoSensor)
    tipo_archivo = models.PositiveSmallIntegerField(
        verbose_name='Tipo de Archivo',
        choices=ARCHIVO_TIPO,
        default=1)
    tipo_reporte = models.PositiveSmallIntegerField(
        verbose_name='Tipo de Reporte',
        choices=REPORTES_TIPO,
        default=1)
    fecha_inicial = models.PositiveIntegerField()
    fecha_final = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    archivo = models.FileField(upload_to=report_files_name)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return self.id

    def sensor_data(self):
        return self.sensor.sensor_data.filter(
            epoch__range=[self.fecha_inicial, self.fecha_final]
        )

    def create_update_file(self):

        buff = BytesIO()
        report = ReportPrint(buff, 'Letter')
        report.print_sensor_data(self)

        # Save the file but don't save the model to avoid
        # loop with self.save method
        self.archivo.save('tmp_name.pdf', File(buff), save=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        # Create the file befor saveing
        self.create_update_file()
        return super(Report, self).save(
            force_insert=False, force_update=False,
            using=None, update_fields=None)


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
