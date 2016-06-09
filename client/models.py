from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Enterprise(models.Model):

    name = models.CharField(verbose_name='Nombre', max_length=55)

    def __unicode__(self):
        return self.name


class Client(models.Model):

    user = models.OneToOneField(User, related_name='client')
    enterprise = models.ForeignKey(Enterprise, related_name='clients')

    def __unicode__(self):
        return self.user.username