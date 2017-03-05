from django.conf.urls import url
from dashboard.views import *
from client.views import CSVReportView, ArduinoAlertDetailView

urlpatterns = [

    url(r'^dash/estatusgeneral/$', SystemStatusListView.as_view(), name="systemstatus"),
    url(r'^dash/projects/$', ProjectsListView.as_view(), name="projects"),
    url(r'^dash/projects/(?P<pk>\d+)/$', ProjectDetailView.as_view(), name="projectDetail"),
    url(r'^dash/reports/(?P<pk>\d+)/$', CSVReportView.as_view(), name="reports"),
    url(r'^dash/alerts/(?P<pk>\d+)/$', ArduinoAlertDetailView.as_view(), name="alerts"),
    url(r'^dash/iot/(?P<pk>\d+)/$', ArduinoDetailView.as_view(), name="arduinoDetail"),
    url(r'^dash/sensor/(?P<pk>\d+)/$', ArduinoSensorDetailView.as_view(), name="sensorDetail"),

    url(r'^dash/(?P<sensor_pk>\d+)/reports/$', ReportListView.as_view(), name='reports-list'),
    url(r'^dash/(?P<sensor_pk>\d+)/reports/add/$', ReportCreateView.as_view(), name='reports-add'),
    url(r'^dash/(?P<sensor_pk>\d+)/reports/detail/(?P<pk>\d+)/$', ReportDetailView.as_view(), name='reports-detail'),
    url(r'^dash/(?P<sensor_pk>\d+)/reports/edit/(?P<pk>\d+)/$', ReportUpdateView.as_view(), name='reports-update'),
    url(r'^dash/(?P<sensor_pk>\d+)/reports/delete/(?P<pk>\d+)/$', ReportDeleteView.as_view(), name='reports-delete'),
]
