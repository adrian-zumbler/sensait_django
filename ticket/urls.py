from django.conf.urls import url, include

from ticket.views import TicketListView, TicketCreateView, TicketUpdateView


urlpatterns = [
    url(r'dash/tickets/$', TicketListView.as_view(), name='ticket-list'),
    url(r'dash/tickets/add/$', TicketCreateView.as_view(), name='ticket-add'),
    url(r'dash/tickets/edit/(?P<pk>\d+)/$', TicketUpdateView.as_view(), name='ticket-edit'),
]
