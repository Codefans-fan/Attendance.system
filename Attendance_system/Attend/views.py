from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core import serializers
# Create your views here.

from models import Attend
from django.contrib.auth.models import User

from base.models import Menu
from base.models import BaseManu

import itertools
import json
import datetime
@login_required(login_url="/user/login")
def index(req):
    menu = __createMenu(req.user)
    context = {
        'menu':menu,
        'userId':req.user.id
        }
    return render(req, "Attend/index.html",context=context)
@login_required(login_url="/user/login")
def show_table_list(req,userid = None):
    if userid is None:
        attends = []
    elif userid == 'all':
        attends =  Attend.objects.filter()
    else:
        attends =  Attend.objects.filter(userId=userid).order_by('lock_time')
    menu = __createMenu(req.user)
    basemenu = []
    basemenu.append(__createMainMenu())
    context = {
        'basemenu':basemenu,
        'menu':menu,
        'lines':attends
        }
    return render(req, "Attend/tablelist.html",context=context)

@login_required(login_url="/user/login")
def show_canlendar(req, type=None, userid=None):
    start = req.GET.get('start')
    end = req.GET.get('end')
    menu = __createMenu(req.user)
    attends = []
    if userid and  start and end:
        attends =  Attend.objects.filter(userId=userid, lock_time__gte = start, lock_time__lt=end).order_by('lock_time')
        return  HttpResponse(serializers.serialize('json', __filter_day_record(attends,True)), content_type="application/json")   
        
    context = {
        'menu':menu,
        'lines':__filter_day_record(attends,True),
        }
    return render(req,"Attend/calendarpage.html",context=context)

def __filter_day_record(records,addHours=False):
    if records:
        res = []
        days_group =[list(group) for k, group in itertools.groupby(records,key=lambda args: args.lock_time.day)]
        for grp in days_group:
            grp.sort(key=lambda p: p.lock_time)
            if len(grp) > 1:
                res.append(grp[0])
                res.append(grp[-1])
                if addHours:
                   timedalta =  grp[-1].lock_time - grp[0].lock_time
                   work_hours = float('%.1f'% (timedalta.total_seconds() / 3600))
                   grp[-1].comment = work_hours
                   grp[-1].save()
            else:
                res.append(grp[0])
        return res
    return []
    

def __createMenu(user):
    menu_1 = Menu('Attend')
    menu_1.addMenu('My attendance','attend_show_table_list('+str(user.id)+')')
    
    if user.has_perm("Attend.readall"):
        menu_1.addMenu('All',"attend_show_table_list('all')")
    
    return (menu_1,)
    
def __createMainMenu():
    mainMenu = BaseManu('Attend','/attend')
    return mainMenu


def clean_attend_database(req):
    users = User.objects.all()
    for user in users:
        attends =  Attend.objects.filter(userId=user.id).order_by('lock_time')
        show_list = __filter_day_record(attends)
        for item in attends:
            if item not in show_list:
                item.delete()
    return HttpResponseRedirect("/")


# def task_weichat_notice(req):
#     users = User.objects.all()
#     for user in users:
#         if user.id == 21:
#             attends =  Attend.objects.filter(userId=user.id,lock_time__gte = datetime.datetime.today().strftime("%Y-%m-%d")).order_by('lock_time')
#             show_list = __filter_day_record(attends)
#             if len(show_list) > 1:
#                 delta_time = show_list[-1].lock_time - show_list[0].lock_time
#                 if delta_time >= datetime.timedelta(hours=9):
#                     print 'lock success'
#                 else:
#                     _weichat_msg()
#             else:
#                 _weichat_msg()
#     return HttpResponseRedirect("/")
# 
# 
# import httplib
# import json
# import urllib
# 
# def _weichat_msg():
#     c = httplib.HTTPSConnection("qyapi.weixin.qq.com")
#     c.request("GET", "/cgi-bin/gettoken?corpid=wx416865667552f10b&corpsecret=60gcQRI8S-1hbMSvqf5CzBnYKBk1O3qOTmPw9Lk37Rxm6bFYifoyu4Me-P5sd53G")
#     response = c.getresponse()
#     #print response.status, response.reason
#     data = response.read()
#     result = json.loads(data)
# 
#     token= result.get('access_token')
#     #print token
#     #send message
#     #https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
# 
#     str_1 = '''{
#    "touser": "@all",
#    "msgtype": "text",
#    "agentid": 0,
#    "text": {
#        "content": "Do not forget to lock out..."
#    },
#    "safe":"0"
#     }'''
#     url = "/cgi-bin/message/send?access_token="+token
# 
#     c.request("POST",url ,str_1)
#     response = c.getresponse()
#     data = response.read()
#     #print data


