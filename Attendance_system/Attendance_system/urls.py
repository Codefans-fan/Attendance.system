"""Attendance_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from base.views import *
from Users.views import login
from Attend.views import index as attend_index
urlpatterns = [
    url(r'^$', index),
    #admin    
    url(r'^admin/', admin.site.urls),
    #base
    url(r'^test', menutest),
   
    # User:
    url(r'^user/login/$', login),
    
    #Attend
    url(r'^attend/',attend_index)
]
