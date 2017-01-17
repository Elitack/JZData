from django.conf.urls import url

from . import views

app_name = 'disk'
urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'^show/$', views.show, name='show'),
    url(r'^download/(?P<fileName>.+)/$', views.download, name='download'),
]
