
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse_lazy

from .models import Enterprise, Client
from .forms import EnterpriseForm, ClientCreationForm, ArduinoSensorCSVReportForm
from arduino.models import Arduino, SensorData
from dashboard.utils.excel_response import ExcelResponse



class EnterpriseListView(LoginRequiredMixin, ListView):
    template_name = 'admin/admin_enterprise_list.html'
    queryset = Enterprise.objects.all()


class EnterpriseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'admin/admin_enterprise_edit.html'
    form_class = EnterpriseForm
    success_url = reverse_lazy('enterprise-client:enterprise-list')


class EnterpriseDetailView(LoginRequiredMixin, DetailView):
    template_name = 'admin/admin_enterprise_detail.html'
    queryset = Enterprise.objects.all()


class EnterpriseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'admin/admin_enterprise_edit.html'
    form_class = EnterpriseForm
    queryset = Enterprise.objects.all()
    success_url = reverse_lazy('enterprise-client:enterprise-list')


class EnterpriseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'admin/admin_enterprise_delete.html'
    success_url = reverse_lazy('enterprise-client:enterprise-list')
    queryset = Enterprise.objects.all()


class ClientListView(LoginRequiredMixin, ListView):
    template_name = 'admin/admin_clients_list.html'
    queryset = Client.objects.all()


class ClientCreateView(LoginRequiredMixin, CreateView):
    template_name = 'admin/admin_client_edit.html'
    form_class = ClientCreationForm
    success_url = reverse_lazy('enterprise-client:client-list')


class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'admin/admin_client_detail.html'
    queryset = Client.objects.all()


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'admin/admin_client_edit.html'
    form_class = ClientCreationForm
    queryset = Client.objects.all()
    success_url = reverse_lazy('enterprise-client:client-list')

    def get_form_kwargs(self):

        kwargs = super(ClientUpdateView, self).get_form_kwargs()
        kwargs.update({'instance': self.object.user,
                       'initial': {
                           'enterprise': self.object.enterprise}
                       })

        return kwargs


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'admin/admin_client_delete.html'
    success_url = reverse_lazy('enterprise-client:client-list')
    queryset = Client.objects.all()


class CSVReportView(SingleObjectMixin, FormView):
    form_class = ArduinoSensorCSVReportForm
    template_name = 'client/user_reports.html'

    def get_queryset(self):

        if self.request.user.is_superuser:
            self.queryset = Arduino.objects.all()
        else:
            self.queryset = Arduino.objects.filter(
                project__clients__user=self.request.user
            )

        return self.queryset

    def get_form_kwargs(self):

        kwargs = super(CSVReportView, self).get_form_kwargs()

        kwargs.update({
            'sensor_queryset': self.object.arduino_sensors.all()
        })

        return kwargs

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        return super(CSVReportView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        objs = SensorData.objects.filter(
            arduino_sensor=form.cleaned_data['sensor'],
            epoch__gte=int(form.cleaned_data['min_time']),
            epoch__lte=int(form.cleaned_data['max_time'])
        ).values('epoch', 'data')
        return ExcelResponse(objs, force_csv=True)


