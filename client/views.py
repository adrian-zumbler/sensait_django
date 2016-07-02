from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.edit import BaseCreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from .models import Enterprise, Client
from .forms import EnterpriseForm, ClientCreationForm


class EnterpriseListView(ListView):
    template_name = 'admin/admin_enterprise_list.html'
    queryset = Enterprise.objects.all()


class EnterpriseCreateView(CreateView):
    template_name = 'admin/admin_enterprise_edit.html'
    form_class = EnterpriseForm
    success_url = reverse_lazy('enterprise-client:enterprise-list')


class EnterpriseDetailView(DetailView):
    template_name = 'admin/admin_enterprise_detail.html'
    queryset = Enterprise.objects.all()


class EnterpriseUpdateView(UpdateView):
    template_name = 'admin/admin_enterprise_edit.html'
    form_class = EnterpriseForm
    queryset = Enterprise.objects.all()
    success_url = reverse_lazy('enterprise-client:enterprise-list')


class EnterpriseDeleteView(DeleteView):
    template_name = 'admin/admin_enterprise_delete.html'
    success_url = reverse_lazy('enterprise-client:enterprise-list')
    queryset = Enterprise.objects.all()


class ClientListView(ListView):
    template_name = 'admin/admin_clients_list.html'
    queryset = Client.objects.all()


class ClientCreateView(CreateView):
    template_name = 'admin/admin_client_edit.html'
    form_class = ClientCreationForm
    success_url = reverse_lazy('enterprise-client:client-list')


class ClientDetailView(DetailView):
    template_name = 'admin/admin_client_detail.html'
    queryset = Client.objects.all()


class ClientUpdateView(UpdateView):
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


class ClientDeleteView(DeleteView):
    template_name = 'admin/admin_client_delete.html'
    success_url = reverse_lazy('enterprise-client:client-list')
    queryset = Client.objects.all()