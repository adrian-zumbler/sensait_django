# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


def client_files_name(instance, filename):
    today = timezone.now()
    today_path = today.strftime('%Y/%m/%d')
    return '/'.join(['clients',
                     today_path,
                     'client_' + str(instance.id),
                     filename])


def client_logo_name(instance, filename):
    today = timezone.now()
    today_path = today.strftime('%Y/%m/%d')
    return '/'.join(['clients',
                     today_path,
                     'client_logo_' + str(instance.id),
                     filename])


class Enterprise(models.Model):

    ESTATUS_CHOICES = (
        (1, 'Contacto'),
        (2, 'Contrato Firmado'),
        (3, 'Revisión de Contrato'),
        (4, 'Pago Pendiente'),
        (5, 'Fin de Relación')
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=55
    )
    nombre_fiscal = models.CharField(
        verbose_name='Nombre Fiscal',
        max_length=55,
        blank=True,
        null=True
    )
    rfc = models.CharField(
        verbose_name='RFC',
        max_length=18,
        blank=True,
        null=True
    )
    direction = models.CharField(
        verbose_name='Dirección Fiscal',
        max_length=255,
        default=''
    )
    city = models.CharField(
        verbose_name='Colonia / Ciudad / Estado',
        max_length=55,
        default=''
    )
    cp = models.CharField(
        verbose_name='Código Postal',
        max_length=8,
        blank=True,
        null=True
    )
    phone_number_1 = models.CharField(
        verbose_name='Teléfono',
        max_length=20,
        default=''
    )
    phone_number_2 = models.CharField(
        verbose_name='Teléfono 2',
        max_length=20,
        blank=True,
        null=True
    )
    email_contact = models.CharField(
        verbose_name='Correo de contacto',
        max_length=300,
        blank=True,
        null=True
    )
    image_logo = models.ImageField(
        verbose_name='Logotipo',
        blank=True,
        upload_to=client_logo_name,
        null=True
    )
    estatus = models.PositiveSmallIntegerField(verbose_name='Estatus', choices=ESTATUS_CHOICES, default=1)

    def __unicode__(self):
        return self.name


class Contacts(models.Model):

    enterprise = models.ForeignKey(Enterprise, related_name='contacts')
    name = models.CharField(
        verbose_name='Nombre',
        max_length=55,
        default=''
    )
    position = models.CharField(
        verbose_name='Puesto',
        max_length=55,
        default=''
    )
    email = models.EmailField(
        verbose_name='Correo electrónico',
        default=''
    )
    phone_number = models.CharField(
        verbose_name='Teléfono',
        max_length=20,
        default=''
    )

    def __unicode__(self):
        return self.name


class Client(models.Model):

    user = models.OneToOneField(User, related_name='client')
    enterprise = models.ForeignKey(Enterprise, related_name='clients')
    profile_pic = models.FileField(
        verbose_name='Foto de perfil',
        upload_to=client_files_name,
        blank=True,
        null=True
    )
    birth_date = models.CharField(
        verbose_name='Fecha de nacimiento',
        max_length=30,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.user.username


class Project(models.Model):

    ESTATUS_CHOICES = (
        (1, 'Levantamiento'),
        (2, 'Diseño'),
        (3, 'Retroalimentación de cliente'),
        (4, 'Implementación'),
        (5, 'Mantenimiento'),
        (6, 'DEMO'),
        (7, 'Activo'),
        (8, 'Alerta')
    )
    PROJECT_CHOICES = (
        (1, 'Demo'),
        (2, 'Laboratorio'),
        (3, 'Clinica'),
        (4, 'Hospital')
    )

    enterprise = models.ForeignKey(Enterprise, related_name='projects')
    clients = models.ManyToManyField(Client, related_name='projects', blank=True) # ForeignKey(Client, related_name='projects', blank=True, null=True)
    name = models.CharField(max_length=255)
    nombre_encargado = models.CharField(
        verbose_name='Nombre Responsable',
        max_length=100,
        blank=True,
        null=True
    )
    cedula_encargado = models.CharField(
        verbose_name='Cédula Profesional',
        max_length=55,
        blank=True,
        null=True
    )
    correo_encargado = models.CharField(
        verbose_name='Correo Encargado',
        max_length=150,
        blank=True,
        null=True
    )
    telefono_encargado = models.CharField(
        verbose_name='Telefono Encargado',
        max_length=55,
        blank=True,
        null=True
    )
    estatus = models.PositiveSmallIntegerField(verbose_name='Estatus', choices=ESTATUS_CHOICES, default=1)

    project_type = models.PositiveSmallIntegerField(verbose_name='Tipo', choices=PROJECT_CHOICES, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


@receiver(post_delete, sender=Client)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
