from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.edit import BaseCreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from .models import Enterprise, Client
from .forms import EnterpriseForm, ClientCreationForm


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
