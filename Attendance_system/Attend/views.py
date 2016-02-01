from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
# Create your views here.

from models import Attend

from base.models import Menu
from base.models import BaseManu

import itertools
import json
from datetime import datetime

@login_required(login_url="/user/login")
def index(req):
    menu = __createMenu(req.user)
    context = {
        'menu':menu,
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
        return  HttpResponse(serializers.serialize('json', __filter_day_record(attends)), content_type="application/json")   
        
    context = {
        'menu':menu,
        'lines':__filter_day_record(attends),
        }
    return render(req,"Attend/calendarpage.html",context=context)

def __filter_day_record(records):
    if records:
        res = []
        days_group =[list(group) for k, group in itertools.groupby(records,key=lambda args: args.lock_time.day)]
        for grp in days_group:
            grp.sort(key=lambda p: p.lock_time)
            res.append(grp[0])
            res.append(grp[-1])
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

