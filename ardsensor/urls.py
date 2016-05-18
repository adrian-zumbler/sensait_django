"""ardsensor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, ListView, DetailView
from arduino.models import Project, Arduino, ArduinoSensor


class ProjectsListView(ListView):
    template_name='client/user_projects.html'
    queryset = Project.objects.all()

    def get_queryset(self):
        queryset = Project.objects.filter(user=self.request.user)
        return queryset

class ProjectDetailView(DetailView):
    template_name='client/user_selected_project.html'
    queryset = Project.objects.all()



class ArduinoDetailView(DetailView):
    template_name='client/user_iots.html'

    def get_queryset(self):
        queryset = Arduino.objects.filter(project__user=self.request.user)
        return queryset


class ArduinoSensorDetailView(DetailView):
    template_name='client/user_selected_sensor.html'

    def get_queryset(self):
        queryset = ArduinoSensor.objects.filter(arduino__project__user=self.request.user)
        return queryset


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('arduino.urls', namespace='arduino', app_name='arduino')),
    url(r'^dash/main', TemplateView.as_view(template_name='client/user_dashboard.html')),
    url(r'^dash/projects/$', ProjectsListView.as_view()),
    url(r'^dash/projects/(?P<pk>\d+)/$', ProjectDetailView.as_view()),
    url(r'^dash/iots/(?P<pk>\d+)/$', ArduinoDetailView.as_view()),
    url(r'^dash/sensor/(?P<pk>\d+)/$', ArduinoSensorDetailView.as_view()),
    url(r'^dash/admin/clients', TemplateView.as_view(template_name='admin/admin_clients.html')),
    url(r'^dash/admin/add', TemplateView.as_view(template_name='admin/admin_clients_add.html'))
] + staticfiles_urlpatterns()
