from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^webhook/$', views.webhook.as_view(),name='whebhook'),
]
