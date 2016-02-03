from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^images/$', views.list_images, name="images"),
    url(r'^taskentry/(?P<task_id>[0-9]+)/$', views.task_entry, name="task_entry"),
    url(r'^logevent/(?P<task_id>[0-9]+)$', views.log_event, name="log_event"),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/' }, name='logout'),
   ]
