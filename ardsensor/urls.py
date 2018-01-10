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

from django.contrib.auth.views import logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static

from django.views.generic import TemplateView


from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout

from dashboard.views import *
from arduino.views import *
from client.views import CSVReportView, ArduinoAlertDetailView

# temporal
from utils.email import EmailView


def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                response_redirect = request.GET.get('next', '/dash/main')
                return HttpResponseRedirect(response_redirect)
    return render_to_response('system/login/login.html', context_instance=RequestContext(request))


#       URLS
# _____________________________________________#
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='landing/index.html'), name="landingPage"),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('arduino.urls', namespace='arduino', app_name='arduino')),
    url(r'^', include('ticket.urls', namespace='ticket')),

    url(r'^', include('dashboard.urls', namespace='dashboard-client')),

    url(r'^dash/', include('client.urls', namespace='enterprise-client')),

    url(r'^dash/main/$', DashMainListView.as_view(), name="main"),

    url(r'^perfil/$', UsuarioPerfil.as_view(), name="miperfil"),

    url(r'^logout/$', logout, {'next': '/'}, name="logout"),
    url(r'^logins/$', login_user),
    url(r'^error/$', TemplateView.as_view(template_name='system/errors/error.html')),

    url(r'^dash/admin/projects/$', AdminProjectsListView.as_view(), name="projectsList"),
    url(r'^dash/admin/projects/detail/(?P<pk>\d+)/$', AdminProjectsDetailView.as_view(), name="projectsDetail"),
    url(r'^dash/admin/projects/new/$', AdminProjectCreateView.as_view(), name="projectsNew"),
    url(r'^dash/admin/projects/edit/(?P<pk>\d+)/$', AdminProjectsEditView.as_view(), name="projectsEdit"),
    url(r'^dash/admin/projects/delete/(?P<pk>\d+)/$', AdminProjectsDeleteView.as_view(), name="projectsDelete"),

    url(r'^dash/admin/Observaciones/$', AdminAlertObservationListView.as_view(), name="alertObservationList"),
    url(r'^dash/admin/Observaciones/new/$', AdminAlertObservationCreateView.as_view(), name="alertObservationNew"),
    url(r'^dash/admin/Observaciones/detail/(?P<pk>\d+)/$', AdminAlertObservationDetailView.as_view(), name="alertObservationDetail"),
    url(r'^dash/admin/Observaciones/edit/(?P<pk>\d+)/$', AdminAlertObservationEditView.as_view(), name="alertObservationEdit"),
    url(r'^dash/admin/Observaciones/delete/(?P<pk>\d+)/$', AdminAlertObservationDeleteView.as_view(), name="alertObservationDelete"),


    url(r'^dash/admin/sensorequipment/$', AdminSensorEquipmentListView.as_view(), name="sensorEquipmentList"),
    url(r'^dash/admin/sensorequipment/new/$', AdminSensorEquipmentCreateView.as_view(), name="sensorEquipmentNew"),
    url(r'^dash/admin/sensorequipment/detail/(?P<pk>\d+)/$', AdminSensorEquipmentDetailView.as_view(), name="sensorEquipmentDetail"),
    url(r'^dash/admin/sensorequipment/edit/(?P<pk>\d+)/$', AdminSensorEquipmentEditView.as_view(), name="sensorEquipmentEdit"),
    url(r'^dash/admin/sensorequipment/delete/(?P<pk>\d+)/$', AdminSensorEquipmentDeleteView.as_view(), name="sensorEquipmentDelete"),

    url(r'^dash/admin/sensortypes/$', AdminSensorTypeListView.as_view(), name="sensorTypeList"),
    url(r'^dash/admin/sensortypes/detail/(?P<pk>\d+)/$', AdminSensorTypeDetailView.as_view(), name="sensorTypeDetail"),
    url(r'^dash/admin/sensortypes/new/$', AdminSensorTypeCreateView.as_view(), name="sensorTypeNew"),
    url(r'^dash/admin/sensortypes/edit/(?P<pk>\d+)/$', AdminSensorTypeEditView.as_view(), name="sensorTypeEdit"),
    url(r'^dash/admin/sensortypes/delete/(?P<pk>\d+)/$', AdminSensorTypeDeleteView.as_view(), name="sensorTypeDelete"),

    url(r'^dash/admin/iots/detail/(?P<pk>\d+)/$', AdminArduinoDetailView.as_view(), name="adminArduinoDetail"),
    url(r'^dash/admin/projects/(?P<project_pk>\d+)/iots/new/$', AdminArduinoCreateView.as_view(), name="newArduino"),
    url(r'^dash/admin/iots/edit/(?P<pk>\d+)/$',
        AdminArduinoWithSensorsUpdateView.as_view(), name="arduinoSensorsEdit"),
    url(r'^dash/admin/iots/delete/(?P<pk>\d+)$', AdminArduinoDeleteView.as_view(), name="arduinoDelete"),
    url(r'^dash/admin/iots/delete/(?P<pk>\d+)/data/$', AdminArduinoDataDeleteView.as_view(), name="arduinoDeleteData"),

    #temporal
    url(r'^emailalerta/(?P<pk>\d+)/$', EmailView.as_view(), name="email"),
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
