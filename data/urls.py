from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^images/$', views.list_images, name="images"),
    url(r'^taskentry/(?P<image_id>[0-9]+)/$', views.task_entry, name="task_entry"),
    url(r'^logevent/(?P<task_id>[0-9]+)$', views.log_event, name="log_event"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/' }, name='logout'),
   ]
