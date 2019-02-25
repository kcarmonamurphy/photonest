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
from django.urls import re_path
from django.conf import settings
from . import views

from re import escape

urlpatterns = [
    re_path(r'^api/v1/get/(?P<path>.*)$', views.get, name='get'),
    re_path(r'^api/v1/peek/(?P<path>.*)$', views.peek, name='peek'),
    re_path(r'^api/v1/thumbnail/(?P<path>.*)$', views.thumbnail, name='thumbnail'),
    re_path(r'^api/v1/full/(?P<path>.*)$', views.full, name='full'),
]
