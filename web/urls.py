from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^image/(?P<image_id>[\w-]+)/$', views.image, name='image'),
    url(r'^instance/(?P<instance_id>[\w-]+)/$', views.instance, name='instance'),
    url(r'^security_groups/', views.security_groups, name='securitygroups'),
    url(r'^overview/', views.overview, name='overview'),
    url(r'^myform/', views.search, name='myform'),
    url(r'^deleterule/(?P<rule_id>[\w-]+)/(?P<instance_id>[\w-]+)/$', views.deleterule, name='deleterule'),
    url(r'^createrule/(?P<secgrp_id>[\w-]+)/(?P<instance_id>[\w-]+)/$', views.createrule, name='createrule'),
]
