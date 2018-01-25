from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name = 'dashboard'),
    url(r'^add$', views.addTask, name='addTask'),
    url(r'^edit/(?P<task_id>\d+)/$', views.edit, name='edit'),
    url(r'^update/(?P<task_id>\d+)$', views.update, name='update'),
    url(r'^delete/(?P<task_id>\d+)/$', views.delete, name='delete'),
]
