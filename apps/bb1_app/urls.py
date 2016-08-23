from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.validation, name='validation'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^travel$', views.index, name='index'),
	url(r'^travel/new$', views.new, name='new'),
	url(r'^travel/(?P<id>\d+)$', views.show, name='show'),
	url(r'^travel/(?P<id>\d+)/edit$', views.edit, name='edit'),
	url(r'^travel/(?P<id>\d+)/destroy$', views.destroy, name='destroy'),
]
