from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy

from ticket.forms import TicketForm, FollowUpForm
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


class TicketDetailView(DetailView):
    template_name = 'ticket/ticket_detail.html'
    queryset = Ticket.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['form'] = FollowUpForm
        return context


class FollowUpCreateView(CreateView):
    form_class = FollowUpForm

    def get_success_url(self):
        return reverse_lazy(
            'tikect:ticket-detail',
            kwargs={'pk': self.form.cleaned_data.ticket.id}
        )

