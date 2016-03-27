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
from Users.views import logout
from Users.views import change_passwd

from Attend.views import index as attend_index
from Attend.views import show_table_list
from Attend.views import show_canlendar
from Attend.views import clean_attend_database
from Attend.views import show_chart

from weichat.views import weichat
from weichat.views import task_weichat_notice


from notice.views import notice_index


from mail.views import mail_index
from mail.views import task_mail_notice
urlpatterns = [
    url(r'^$', index),
    #admin    
    url(r'^admin/', admin.site.urls),
    #base
    url(r'^test', menutest),
    url(r'^donate',donate),
    # User:
    url(r'^user/login/*', login, name='login'),
    url(r'^user/logout/$', logout, name='logout'),
    url(r'^user/changepw/$',change_passwd),
    
    #Attend
    url(r'^attend/$',attend_index),
    url(r'^attend/id=([0-9]+)',show_table_list),
    url(r'^attend/id=(all)',show_table_list),
    url(r'^attend/type=1&id=([0-9]+)$',show_canlendar),
    url(r'^attend/clean_attend_database',clean_attend_database),
    url(r'^attend/type=2&id=([0-9]+)$',show_chart),
    
    #weichat
    url(r'^weichat/$',weichat),
    url(r'^weichat/task_weichat_notice',task_weichat_notice),
    #url(r'^attend/type=([0-9])&id=([0-9]+)&start=(\d{4}-\d{2}-\d{2})&end=(\d{4}-\d{2}-\d{2})',show_canlendar),
    
    #notice
    url(r'^notice/$',notice_index),
    

    #mail
    url(r'^email/$',mail_index),
    url(r'^email/task_mail_notice',task_mail_notice)

]
