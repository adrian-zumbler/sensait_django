from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy

from ticket.forms import TicketForm
from helpdesk.models import Ticket


class TicketListView(ListView):
    template_name = 'ticket/ticket_list.html'
    model = Ticket
    queryset = Ticket.objects.all()


class TicketCreateView(CreateView):
    template_name = 'ticket/ticket_edit.html'
    form_class = TicketForm
    success_url = reverse_lazy('ticket:ticket-list')


class TicketUpdateView(UpdateView):
    template_name = 'ticket/ticket_edit.html'
    form_class = TicketForm
    success_url = reverse_lazy('ticket:ticket-list')
    queryset = Ticket.objects.all()
