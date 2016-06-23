from django.conf.urls import url

from .views import EnterpriseListView, EnterpriseCreateView, EnterpriseDetailView,  \
    ClientListView, ClientCreateView


urlpatterns = [
    url(r'^admin/enterprises/$', EnterpriseListView.as_view(), name='enterprise-list'),
    url(r'^admin/enterprises/add/$', EnterpriseCreateView.as_view(), name='enterprise-add'),
    url(r'^admin/enterprises/detail/(?P<pk>\d+)/$', EnterpriseDetailView.as_view(), name='enterprise-detail'),
    url(r'^admin/clients/$', ClientListView.as_view(), name='client-list'),
    url(r'^admin/clients/add/$', ClientCreateView.as_view(), name='client-add')
]
