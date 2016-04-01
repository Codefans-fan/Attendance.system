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
from datetime import timedelta
import types
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
        attends =  Attend.objects.filter(userId=userid).order_by('-lock_time')[:1000]
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
def show_canlendar(req, userid=None):
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


@login_required(login_url="/user/login")
def show_chart(req, userid=None):
    day = '2016-03-10'
    # datetime.datetime.strptime(day, '%Y-%m-%d')
    today = datetime.datetime.strptime(day, '%Y-%m-%d')  #datetime.datetime.now().date()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    
    attends =  Attend.objects.filter(userId=userid, lock_time__gte = start, lock_time__lt=end).order_by('lock_time')
    
    context = {
        'items':__get_workHours(__filter_day_record(attends, True))
    }
    return render(req,"Attend/chart.html",context = context)


def __get_workHours(records):
    items = []
    for line in records:
        if type(line.comment) == types.FloatType or type(line.comment) == types.IntType:
            items.append(line.comment)
    return items
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
                   if not grp[-1].comment.isdigit():
                       grp[-1].comment  = work_hours
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

