from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views.generic.edit import BaseCreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

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


class FollowUpCreateView(BaseCreateView):
    form_class = FollowUpForm

    def post(self, request, *args, **kwargs):
        self.object = None
        return super(BaseCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.ticket = Ticket.objects.get(id=self.kwargs['pk'])
        return super(FollowUpCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.INFO, 'Tu comentario es invalido.')
        return self.form_valid(form)


    def get_success_url(self):
        return reverse_lazy(
            'ticket:ticket-detail',
            kwargs={'pk': self.kwargs['pk']}
        )

