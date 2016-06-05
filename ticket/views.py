from django.shortcuts import render
from django.views.generic import ListView

from helpdesk.models import Ticket

class TicketListView(ListView):
    template_name = 'ticket/ticket_list.html'
    model = Ticket
    queryset = Ticket.objects.all()