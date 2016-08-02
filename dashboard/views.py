from django.shortcuts import render

from django import forms
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse

from dashboard.forms import AdminArduinoCreateForm, AdminProjectUpdateForm, \
    AdminProjectCreateForm, ArduinoSensorFormSet
from arduino.models import Arduino, ArduinoSensor
from client.models import Project, Client


#       CLASES PARA USUARIO/CLIENTE
# _____________________________________________#
class ProjectsListView(ListView):
    template_name = 'client/user_projects.html'
    queryset = Project.objects.all()

    def get_queryset(self):
        queryset = Project.objects.all()  # .filter(user=self.request.user)
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
        # TODO: Filtrar por clientes permitios
        queryset = Project.objects.all()  # filter(user=self.request.user)
        return queryset


#       ADMIN - PROYECTOS
# _____________________________________________#
class AdminProjectsListView(ListView):
    template_name = 'admin/admin_projects_list.html'
    queryset = Project.objects.all()


class AdminProjectsDetailView(DetailView):
    template_name = 'admin/admin_projects_detail.html'
    queryset = Project.objects.all()

    def get_context_data(self, **kwargs):

        context = super(AdminProjectsDetailView, self).get_context_data(**kwargs)

        tipo = type(self.object)

        proj = Project.objects.get(id=self.object.id)

        context['arduinos'] = Arduino.objects.filter(project_id=proj.id)

        return context


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
class AdminArduinoCreateView(CreateView):
    form_class = AdminArduinoCreateForm
    template_name = 'admin/admin_arduinos_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = Project.objects.get(
            id=self.kwargs['project_pk']
        )
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('projectsDetail', kwargs={'pk': self.object.project.id})

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = self.initial.copy()
        initial['project'] = self.kwargs['project_pk']
        return initial


class AdminArduinoWithSensorsUpdateView(UpdateView):
    form_class = AdminArduinoCreateForm
    template_name = 'admin/admin_arduinowithsensors_update.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        sensor_formset = ArduinoSensorFormSet(request.POST)
        if form.is_valid() and sensor_formset.is_valid():
            return self.form_valid(form, sensor_formset)
        else:
            return self.form_invalid(form, sensor_formset)

    def form_valid(self, form, sensor_formset):
        self.object = form.save()
        sensors = sensor_formset.save(commit=False)
        for sensor in sensors:
            sensor.arduino = self.object
            sensor.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, sensor_formset):
        return self.render_to_response(
            self.get_context_data(form=form, sensor_formset=sensor_formset)
        )

    def get_context_data(self, **kwargs):

        ctx = super(AdminArduinoWithSensorsUpdateView, self).get_context_data(**kwargs)
        # qs = ArduinoSensor.objects.filter(
        #     arduino=self.object
        # )  # self.object.sensors.all()
        ctx['sensor_formset'] = ArduinoSensorFormSet(
            queryset=self.object.arduinosensor_set.all()
        )
        return ctx

    def get_success_url(self):

        return reverse('projectsDetail', kwargs={'pk': self.object.project.id})

    def get_queryset(self):

        qs = Arduino.objects.all()

        return qs


