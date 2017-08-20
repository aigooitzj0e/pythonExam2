from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^reg_process$', views.reg_process),
    url(r'^dashboard$', views.dashboard),
    url(r'^login_process$', views.login_process),
    url(r'^logout/$', views.logout),
    url(r'^additem/$', views.additem),
    url(r'^additem_process$', views.additem_process),
    url(r'^delete/(?P<iid>\d+)$', views.delete),
    url(r'^show/(?P<iid>\d+)$', views.show),
    url(r'^join/(?P<iid>\d+)$', views.join),
    url(r'^remove/(?P<iid>\d+)$', views.remove),
]
