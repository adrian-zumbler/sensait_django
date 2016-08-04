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
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static

from django.views.generic import TemplateView


from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from dashboard.views import *

def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dash/main')
    return render_to_response('system/login/login.html', context_instance=RequestContext(request))


#       URLS
# _____________________________________________#
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('arduino.urls', namespace='arduino', app_name='arduino')),
    url(r'^', include('ticket.urls', namespace='ticket')),
    url(r'^dash/', include('client.urls', namespace='enterprise-client')),

    url(r'^logins/$', login_user),
    url(r'^error/$', TemplateView.as_view(template_name='system/errors/error.html')),

    url(r'^dash/main/$', DashMainListView.as_view(), name="main"),
    url(r'^dash/projects/$', ProjectsListView.as_view(), name="projects"),
    url(r'^dash/projects/(?P<pk>\d+)/$', ProjectDetailView.as_view(), name="projectDetail"),
    url(r'^dash/iot/(?P<pk>\d+)/$', ArduinoDetailView.as_view(), name="arduinoDetail"),
    url(r'^dash/sensor/(?P<pk>\d+)/$', ArduinoSensorDetailView.as_view(), name="sensorDetail"),




    url(r'^dash/admin/clients/$', TemplateView.as_view(template_name='admin/admin_clients.html'), name="clientsList"),
    url(r'^dash/admin/projects/$', AdminProjectsListView.as_view(), name="projectsList"),
    url(r'^dash/admin/projects/detail/(?P<pk>\d+)/$', AdminProjectsDetailView.as_view(), name="projectsDetail"),
    url(r'^dash/admin/projects/new/$', AdminProjectCreateView.as_view(), name="projectsNew"),
    url(r'^dash/admin/projects/edit/(?P<pk>\d+)/$', AdminProjectsEditView.as_view(), name="projectsEdit"),
    url(r'^dash/admin/projects/delete/(?P<pk>\d+)/$', AdminProjectsDeleteView.as_view(), name="projectsDelete"),
    url(r'^dash/admin/projects/(?P<project_pk>\d+)/iot/new/$', AdminArduinoCreateView.as_view(), name="newArduino"),
    url(r'^dash/admin/iot/edit/(?P<pk>\d+)/$',
        AdminArduinoWithSensorsUpdateView.as_view(), name="arduinoSensorsEdit"),
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
