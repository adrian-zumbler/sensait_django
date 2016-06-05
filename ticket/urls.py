from django.conf.urls import url, include

from ticket.views import TicketListView


urlpatterns = [
    url(r'dash/tickets/$', TicketListView.as_view(), name='ticket-list'),
]
