from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
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


class ClientListView(ListView):
    template_name = 'admin/admin_clients_list.html'
    queryset = Client.objects.all()


class ClientCreateView(CreateView):
    template_name = 'admin/admin_client_edit.html'
    form_class = ClientCreationForm
    success_url = reverse_lazy('enterprise-client:client-list')
