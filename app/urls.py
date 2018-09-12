"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

from rest_framework import routers, serializers, viewsets

from . import views
import re

router = routers.DefaultRouter()
router.register(r'images', views.ImageViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),

    # url(r'^' + re.escape(settings.GALLERY_PREFIX) + '/(?P<relative_path>.*)$', views.index, name='index'),
    # url(r'^template/(?P<template>.*)$', views.template, name='template'),
    # url(r'^api/(?P<relative_path>.*)$', )
]
