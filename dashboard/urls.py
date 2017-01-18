from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from django.contrib.auth.views import logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static

from django.views.generic import TemplateView
from django.template import RequestContext

from dashboard.views import *
from arduino.views import *
from client.views import CSVReportView, ArduinoAlertDetailView

urlpatterns = [

    url(r'^dash/status/$', SystemStatusListView.as_view(), name="status"),
    url(r'^dash/projects/$', ProjectsListView.as_view(), name="projects"),
    url(r'^dash/projects/(?P<pk>\d+)/$', ProjectDetailView.as_view(), name="projectDetail"),
    url(r'^dash/reports/(?P<pk>\d+)/$', CSVReportView.as_view(), name="reports"),
    url(r'^dash/alerts/(?P<pk>\d+)/$', ArduinoAlertDetailView.as_view(), name="alerts"),
    url(r'^dash/iot/(?P<pk>\d+)/$', ArduinoDetailView.as_view(), name="arduinoDetail"),
    url(r'^dash/sensor/(?P<pk>\d+)/$', ArduinoSensorDetailView.as_view(), name="sensorDetail")

    # url(r'^dash/reports/$', EnterpriseListView.as_view(), name='reports-list'),
    # url(r'^dash/reports/add/$', EnterpriseCreateView.as_view(), name='reports-add'),
    # url(r'^dash/reports/detail/(?P<pk>\d+)/$', EnterpriseDetailView.as_view(), name='reports-detail'),
    # url(r'^dash/reports/edit/(?P<pk>\d+)/$', EnterpriseUpdateView.as_view(), name='reports-update'),
    # url(r'^dash/reports/delete/(?P<pk>\d+)/$', EnterpriseDeleteView.as_view(), name='reports-delete'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
