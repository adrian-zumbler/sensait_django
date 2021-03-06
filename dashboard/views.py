
from io import BytesIO

from django import forms
from django.core.files import File
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from dashboard.forms import AdminArduinoCreateForm, AdminProjectUpdateForm, \
    AdminProjectCreateForm, ArduinoSensorFormSet, InLineArduinoSensorFormSet, ReportForm
from arduino.models import Arduino, ArduinoSensor, Report
from client.models import Project, Client
from ardsensor.printing import ReportPrint


#       CLASES PARA USUARIO/CLIENTE
# _____________________________________________#
class ProjectsListView(LoginRequiredMixin, ListView):
    template_name = 'client/user_projects.html'
    queryset = Project.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.none()
        if hasattr(user, 'client'):
            client = user.client
            queryset = client.projects.all()
        elif user.is_staff:
            queryset = Project.objects.all()
        # queryset = Project.objects.all()  # .filter(user=self.request.user)
        return queryset


class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = 'client/user_selected_project.html'
    queryset = Project.objects.all()


class ArduinoDetailView(LoginRequiredMixin, DetailView):
    template_name = 'client/user_iots.html'

    def get_context_data(self, **kwargs):
        context = super(ArduinoDetailView, self).get_context_data(**kwargs)
        context['site_url'] = self.request.get_host()
        # build_absolute_uri('/')
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Arduino.objects.none()
        if hasattr(user, 'client'):
            queryset = Arduino.objects.filter(project__clients__user=user)
        elif user.is_staff:
            queryset = Arduino.objects.all()

        return queryset


class ArduinoSensorDetailView(LoginRequiredMixin, DetailView):
    template_name = 'client/user_selected_sensor.html'

    def get_context_data(self, **kwargs):
        context = super(ArduinoSensorDetailView, self).get_context_data(**kwargs)
        context['site_url'] = self.request.get_host()
        # build_absolute_uri('/')
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = ArduinoSensor.objects.none()
        if hasattr(user, 'client'):
            queryset = ArduinoSensor.objects.filter(arduino__project__clients__user=self.request.user)
        elif user.is_staff:
            queryset = ArduinoSensor.objects.all()

        return queryset


class UsuarioPerfil(LoginRequiredMixin, DetailView):
    template_name = 'client/user_profile.html'
    """
    def get_queryset(self):
        queryset = self.request.user
    """


class DashMainListView(LoginRequiredMixin, ListView):
    template_name = 'client/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashMainListView, self).get_context_data(**kwargs)

        context['site_url'] = self.request.get_host()
        context['holo'] = self.request.get_host()
        # request.get_host('/')
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.none()
        if hasattr(user, 'client'):
            client = user.client
            queryset = client.projects.all()
        elif user.is_staff:
            queryset = Project.objects.all()

        return queryset.order_by('-created_at')


class SystemStatusListView(LoginRequiredMixin, ListView):
    template_name = 'client/user_systemstatus.html'

    def get_context_data(self, **kwargs):
        context = super(SystemStatusListView, self).get_context_data(**kwargs)

        context['site_url'] = self.request.get_host()
        context['holo'] = self.request.get_host()
        # request.get_host('/')
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.none()
        if hasattr(user, 'client'):
            client = user.client
            queryset = client.projects.all()
        elif user.is_staff:
            queryset = Project.objects.all()

        return queryset.order_by('-created_at')

#       ADMIN - PROYECTOS
# _____________________________________________#


class UserProjectListView(LoginRequiredMixin, ListView):
    template_name = 'client/user_project_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            qs = Project.objects.all()
        else:
            qs = self.request.user.client.projects
        return qs

#       ADMIN - PROYECTOS
# _____________________________________________#


class AdminProjectsListView(LoginRequiredMixin, ListView):
    template_name = 'admin/admin_projects_list.html'
    queryset = Project.objects.all()
"""
    def get_context_data(self, **kwargs):
        context = super(AdminProjectsListView, self).get_context_data(**kwargs)
        tipo = type(self.object)
        proj = Project.objects.get(id=self.object.id)
        context['arduinos'] = Arduino.objects.filter(project_id=proj.id)
        return context
"""

class AdminProjectsDetailView(LoginRequiredMixin, DetailView):
    template_name = 'admin/admin_projects_detail.html'
    queryset = Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AdminProjectsDetailView, self).get_context_data(**kwargs)
        tipo = type(self.object)
        proj = Project.objects.get(id=self.object.id)
        context['arduinos'] = Arduino.objects.filter(project_id=proj.id)
        return context


class AdminProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = AdminProjectCreateForm
    template_name = 'admin/admin_projects_create.html'
    success_url = reverse_lazy('projectsList')


class AdminProjectsEditView(LoginRequiredMixin, UpdateView):
    form_class = AdminProjectUpdateForm
    template_name = 'admin/admin_projects_create.html'
    success_url = reverse_lazy('projectsList')
    queryset = Project.objects.all()


class AdminProjectsDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'admin/admin_projects_delete.html'
    success_url = reverse_lazy('projectsList')
    queryset = Project.objects.all()


#       ADMIN - ARDUINOS
# _____________________________________________#
class AdminArduinoCreateView(LoginRequiredMixin, CreateView):
    form_class = AdminArduinoCreateForm
    template_name = 'admin/admin_arduino_create.html'

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


class AdminArduinoWithSensorsUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AdminArduinoCreateForm
    template_name = 'admin/admin_arduinowithsensors_update.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        sensor_formset = InLineArduinoSensorFormSet(data=request.POST, instance=self.object)
        if form.is_valid() and sensor_formset.is_valid():
            return self.form_valid(form, sensor_formset)
        else:
            return self.form_invalid(form, sensor_formset)

    def form_valid(self, form, sensor_formset):
        self.object = form.save()
        sensors = sensor_formset.save()
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
        queryset = self.object.arduino_sensors.all()
        ctx['sensor_formset'] = InLineArduinoSensorFormSet(
            instance=self.object
        )
        return ctx

    def get_success_url(self):
        return reverse('projectsDetail', kwargs={'pk': self.object.project.id})

    def get_queryset(self):
        qs = Arduino.objects.all()
        return qs


class ReportListView(LoginRequiredMixin, ListView):
    template_name = 'client/client_report_list.html'
    # queryset = Report.objects.all()

    def get_queryset(self):
        return Report.objects.filter(
            sensor_id=self.kwargs['sensor_pk']
        )

    def get_context_data(self, **kwargs):
        ctx = super(ReportListView, self).get_context_data(**kwargs)
        ctx.update(self.kwargs)
        return ctx


class ReportCreateView(LoginRequiredMixin, CreateView):
    template_name = 'client/client_report_edit.html'
    form_class = ReportForm

    def get_success_url(self):
        return reverse_lazy(
            'dashboard-client:reports-list',
            kwargs={'sensor_pk': self.kwargs['sensor_pk']}
        )

    def get_context_data(self, **kwargs):
        ctx = super(ReportCreateView, self).get_context_data(**kwargs)
        ctx.update(self.kwargs)
        return ctx

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sensor_id = self.kwargs['sensor_pk']
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ReportDetailView(LoginRequiredMixin, DetailView):
    template_name = 'client/client_report_detail.html'
    queryset = Report.objects.all()


class ReportUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'client/client_report_edit.html'
    form_class = ReportForm
    queryset = Report.objects.all()

    def get_success_url(self):
        return reverse_lazy(
            'dashboard-client:reports-list',
            kwargs={'sensor_pk': self.kwargs['sensor_pk']}
        )

    def get_context_data(self, **kwargs):
        ctx = super(ReportUpdateView, self).get_context_data(**kwargs)
        ctx.update(self.kwargs)
        return ctx


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'client/client_report_delete.html'
    success_url = reverse_lazy('dashboard-client:reports-list')
    queryset = Report.objects.all()

    def get_success_url(self):
        return reverse_lazy(
            'dashboard-client:reports-list',
            kwargs={'sensor_pk': self.kwargs['sensor_pk']}
        )
