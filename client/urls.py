from django.conf.urls import url

from .views import EnterpriseListView, EnterpriseCreateView, EnterpriseDetailView,  \
    EnterpriseUpdateView, EnterpriseDeleteView, ClientListView, ClientCreateView,  \
    ClientDetailView, ClientUpdateView, ClientDeleteView


urlpatterns = [
    url(r'^admin/enterprises/$', EnterpriseListView.as_view(), name='enterprise-list'),
    url(r'^admin/enterprises/add/$', EnterpriseCreateView.as_view(), name='enterprise-add'),
    url(r'^admin/enterprises/detail/(?P<pk>\d+)/$', EnterpriseDetailView.as_view(), name='enterprise-detail'),
    url(r'^admin/enterprises/edit/(?P<pk>\d+)/$', EnterpriseUpdateView.as_view(), name='enterprise-update'),
    url(r'^admin/enterprises/delete/(?P<pk>\d+)/$', EnterpriseDeleteView.as_view(), name='enterprise-delete'),
    url(r'^admin/clients/$', ClientListView.as_view(), name='client-list'),
    url(r'^admin/clients/add/$', ClientCreateView.as_view(), name='client-add'),
    url(r'^admin/clients/detail/(?P<pk>\d+)/$', ClientDetailView.as_view(), name='client-detail'),
    url(r'^admin/clients/edit/(?P<pk>\d+)/$', ClientUpdateView.as_view(), name='client-update'),
    url(r'^admin/clients/delete/(?P<pk>\d+)/$', ClientDeleteView.as_view(), name='client-delete'),
]
