from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Enterprise(models.Model):

    name = models.CharField(verbose_name='Nombre', max_length=55)

    def __unicode__(self):
        return self.name


class Client(models.Model):

    user = models.OneToOneField(User, related_name='client')
    enterprise = models.ForeignKey(Enterprise, related_name='clients')

    def __unicode__(self):
        return self.user.username


class Project(models.Model):
    enterprise = models.ForeignKey(Enterprise)
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
