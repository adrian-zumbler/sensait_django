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
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django import forms
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from arduino.models import Project, Arduino, ArduinoSensor


#       CLASES PARA USUARIO/CLIENTE
#_____________________________________________#

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



#       CLASES PARA ADMIN
#_____________________________________________#


#       ADMIN - PROYECTOS
#_____________________________________________#
class AdminProjectsListView(ListView):
    template_name='admin/admin_projects.html'
    queryset = Project.objects.all()


class AdminProjectsDetailView(DetailView):
    template_name='admin/admin_projects_detail.html'
    queryset = Project.objects.all()

    #def get_queryset(self):
    #    print self.kwargs
    #    queryset = Project.objects.filter(project__user=self.request.user)
        #queryset = Project.objects.filter(project_id=self.kwargs['pk'])
#        print queryset
#        return queryset


class AdminProjectCreateForm(forms.ModelForm):
    name = forms.RegexField(r'[A-Za-z]+')

    class Meta:
        model = Project
        fields = '__all__'


class AdminProjectCreateView(CreateView):
    form_class = AdminProjectCreateForm
    template_name = 'admin/admin_projects_create.html'
    success_url = reverse_lazy('adminListProjects')


class AdminProjectsEditView(UpdateView):
    form_class = AdminProjectCreateForm
    template_name = 'admin/admin_projects_create.html'
    success_url = reverse_lazy('adminListProjects')
    queryset = Project.objects.all()


class AdminProjectsDeleteView(DeleteView):
    template_name = 'admin/admin_projects_delete.html'
    success_url = reverse_lazy('adminListProjects')
    queryset = Project.objects.all()


#       ADMIN - ARDUINOS
#_____________________________________________#


class AdminArduinoCreateForm(forms.ModelForm):
    name = forms.RegexField(r'[A-Za-z]+')

    class Meta:
        model   = Arduino
        fields  = ['name', 'location', 'project']


class AdminArduinoCreateView(CreateView):
    form_class = AdminArduinoCreateForm
    template_name = 'admin/admin_arduinos_create.html'

    def get_success_url(self):
        return reverse('adminDetailProjects', kwargs={'pk': self.kwargs['project_pk']})

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = self.initial.copy()
        initial['project'] = self.kwargs['project_pk']
        return initial



#       URLS
#_____________________________________________#

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('arduino.urls', namespace='arduino', app_name='arduino')),
    url(r'^dash/main', TemplateView.as_view(template_name='client/user_dashboard.html')),
    url(r'^dash/projects/$', ProjectsListView.as_view()),
    url(r'^dash/projects/(?P<pk>\d+)/$', ProjectDetailView.as_view()),
    url(r'^dash/iot/(?P<pk>\d+)/$', ArduinoDetailView.as_view()),
    url(r'^dash/sensor/(?P<pk>\d+)/$', ArduinoSensorDetailView.as_view()),
    url(r'^dash/admin/clients/$', TemplateView.as_view(template_name='admin/admin_clients.html')),
    url(r'^dash/admin/projects/$', AdminProjectsListView.as_view(), name='adminListProjects'),
    url(r'^dash/admin/projects/detail/(?P<pk>\d+)/$', AdminProjectsDetailView.as_view(), name='adminDetailProjects'),
    url(r'^dash/admin/projects/new/$', AdminProjectCreateView.as_view(), name='adminCreateProjects'),
    url(r'^dash/admin/projects/edit/(?P<pk>\d+)/$', AdminProjectsEditView.as_view(), name='adminEditProjects'),
    url(r'^dash/admin/projects/delete/(?P<pk>\d+)/$', AdminProjectsDeleteView.as_view(), name='adminDeleteProjects'),
    url(r'^dash/admin/projects/(?P<project_pk>\d+)/iot/new/$', AdminArduinoCreateView.as_view(), name='adminCreateArduinos'),
] + staticfiles_urlpatterns()
