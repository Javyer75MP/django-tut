from django.conf.urls import include, url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.PostList.as_view(), name='post_list'),
    url(r'^post/new/$', views.PostCreate.as_view(), name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetail.as_view(), name='post_detail'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^about/', TemplateView.as_view(template_name="about.html"),name='about'),
]
  