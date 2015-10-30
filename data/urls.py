from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^menus/$', views.list_menus, name="menus"),
    url(r'^menuentry/(?P<menu_id>[0-9]+)/$', views.menu_entry, name="menu_entry"),
    url(r'^logevent/(?P<menu_id>[0-9]+)$', views.log_event, name="log_event"),
]
