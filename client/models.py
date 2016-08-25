# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


def client_files_name(instance, filename):
    today = timezone.now()
    today_path = today.strftime('%Y/%m/%d')
    return '/'.join(['clients',
                     today_path,
                     'client_' + str(instance.id),
                     filename])


class Enterprise(models.Model):

    name = models.CharField(verbose_name='Nombre', max_length=55)
    direction = models.CharField(
        verbose_name='Dirección',
        max_length=255,
        default=''
    )
    city = models.CharField(
        verbose_name='Ciudad-Estado',
        max_length=55,
        default=''
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
    enterprise = models.ForeignKey(Enterprise, related_name='projects')
    clients = models.ManyToManyField(Client, related_name='projects', blank=True) # ForeignKey(Client, related_name='projects', blank=True, null=True)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


@receiver(post_delete, sender=Client)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user:  # just in case user is not specified
        instance.user.delete()
