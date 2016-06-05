from django.conf.urls import url, include

from ticket.views import TicketListView, TicketCreateView


urlpatterns = [
    url(r'dash/tickets/$', TicketListView.as_view(), name='ticket-list'),
    url(r'dash/tickets/add/$', TicketCreateView.as_view(), name='ticket-add'),
]
