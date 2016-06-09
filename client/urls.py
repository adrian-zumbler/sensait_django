from django.conf.urls import url

from .views import EnterpriseListView, EnterpriseCreateView, \
    ClientListView, ClientCreateView


urlpatterns = [
    url(r'^enterprises/$', EnterpriseListView.as_view(), name='enterprise-list'),
    url(r'^enterprises/add/$', EnterpriseCreateView.as_view(), name='enterprise-add'),
    url(r'^clients/$', ClientListView.as_view(), name='client-list'),
    url(r'^clients/add/$', ClientCreateView.as_view(), name='client-add')
]
