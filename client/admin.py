from django.contrib import admin
from client.models import Enterprise, Client, Project

# Register your models here.

admin.site.register(Enterprise)
admin.site.register(Client)
admin.site.register(Project)
