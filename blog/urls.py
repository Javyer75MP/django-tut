from django.conf.urls import include, url
from . import  views

url patterns = [
    url(r'^$', views.post_list),
    ]   