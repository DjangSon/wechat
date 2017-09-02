from django.conf.urls import url
from manager import views

urlpatterns = [
    url(r'^$', views.index),
]