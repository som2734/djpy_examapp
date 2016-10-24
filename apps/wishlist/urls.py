from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^profile$', views.profile),
    url(r'^create_item$', views.create_item),
    url(r'^create$', views.create),
    url(r'^profile$', views.profile),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^add_wl/(?P<id>\d+)$', views.add_wl),
    url(r'^show_item/(?P<id>\d+)$', views.show_item),
]
