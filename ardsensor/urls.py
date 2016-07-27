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
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles.urls import static
from django import forms
from django.forms.utils import ErrorList
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from arduino.models import Arduino, ArduinoSensor
from client.models import Project, Client

from django.http import *
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


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

#       CLASES PARA USUARIO/CLIENTE
# _____________________________________________#


class ProjectsListView(ListView):
    template_name = 'client/user_projects.html'
    queryset = Project.objects.all()

    def get_queryset(self):
        queryset = Project.objects.filter(user=self.request.user)
        return queryset


class ProjectDetailView(DetailView):
    template_name = 'client/user_selected_project.html'
    queryset = Project.objects.all()


class ArduinoDetailView(DetailView):
    template_name = 'client/user_iots.html'

    def get_queryset(self):
        queryset = Arduino.objects.filter(project__user=self.request.user)
        return queryset


class ArduinoSensorDetailView(DetailView):
    template_name = 'client/user_selected_sensor.html'

    def get_queryset(self):
        queryset = ArduinoSensor.objects.filter(arduino__project__user=self.request.user)
        return queryset


class DashMainListView(ListView):
    template_name = 'client/user_dashboard.html'
    queryset = Project.objects.all()

    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset


#       CLASES PARA ADMIN filter(user=self.request.user)
# _____________________________________________#


#       ADMIN - PROYECTOS
# _____________________________________________#
class AdminProjectsListView(ListView):
    template_name = 'admin/admin_projects_list.html'
    queryset = Project.objects.all()


class AdminProjectsDetailView(DetailView):
    template_name = 'admin/admin_projects_detail.html'
    queryset = Project.objects.all()


class AdminProjectCreateForm(forms.ModelForm):
    name = forms.RegexField(r'[A-Za-z]+')

    class Meta:
        model = Project
        exclude = ('clients', )


class AdminProjectUpdateForm(forms.ModelForm):
    name = forms.RegexField(r'[A-Za-z]+')

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):
        super(AdminProjectUpdateForm, self).__init__(
            data, files, auto_id, prefix, initial, error_class,
            label_suffix, empty_permitted, instance)
        queryset = Client.objects.filter(enterprise=instance.enterprise)
        self.fields['clients'] = forms.ModelChoiceField(
            queryset=queryset
        )
        clients = self.fields


class Meta:
        model = Project
        fields = '__all__'


class AdminProjectCreateView(CreateView):
    form_class = AdminProjectCreateForm
    template_name = 'admin/admin_projects_create.html'
    success_url = reverse_lazy('projectsList')


class AdminProjectsEditView(UpdateView):
    form_class = AdminProjectUpdateForm
    template_name = 'admin/admin_projects_create.html'
    success_url = reverse_lazy('projectsList')
    queryset = Project.objects.all()


class AdminProjectsDeleteView(DeleteView):
    template_name = 'admin/admin_projects_delete.html'
    success_url = reverse_lazy('projectsList')
    queryset = Project.objects.all()


#       ADMIN - ARDUINOS
# _____________________________________________#


class AdminArduinoCreateForm(forms.ModelForm):
    name = forms.RegexField(r'[A-Za-z]+')

    class Meta:
        model = Arduino
        fields = ['name', 'location', 'project']


class AdminArduinoCreateView(CreateView):
    form_class = AdminArduinoCreateForm
    template_name = 'admin/admin_arduinos_create.html'

    def get_success_url(self):
        return reverse('projectsDetail', kwargs={'pk': self.kwargs['project_pk']})

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = self.initial.copy()
        initial['project'] = self.kwargs['project_pk']
        return initial


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
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
