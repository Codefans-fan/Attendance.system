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
from holiday.models import holiday_cn

import datetime
from itertools import chain
from base import attendance_utils
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
def show_canlendar(req, type=1, id=None):
    start = req.GET.get('start')
    end = req.GET.get('end')
    menu = __createMenu(req.user)
    attends = []
    if start and end:
        attends =  Attend.objects.filter(userId=req.user.id, lock_time__gte = start, lock_time__lt=end).order_by('lock_time')
        holiday = holiday_cn.objects.filter(day__gte=start,day__lt=end)
        v_attends = attendance_utils.filter_day_record(attends,True)
        res = chain(holiday,v_attends)
        return  HttpResponse(serializers.serialize('json', res ), content_type="application/json")   
    context = {
        'menu':menu,
        'lines':attendance_utils.filter_day_record(attends,True),
        }
    return render(req,"Attend/calendarpage.html",context=context)


@login_required(login_url="/user/login")
def show_chart(req,type=2, id=None):
    # datetime.datetime.strptime(day, '%Y-%m-%d')
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0)
    yesterday = today -datetime.timedelta(days=1)
    attends =  Attend.objects.filter(lock_time__gte = yesterday, lock_time__lt=today).order_by('lock_time')
    context = {
        'items':attendance_utils.get_workHours(attends)
    }
    return render(req,"Attend/chart.html",context = context)

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
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0)
    for user in users:
        attends =  Attend.objects.filter(userId=user.id,lock_time__gte = today).order_by('lock_time')
        show_list = attendance_utils.filter_day_record(attends,True)
        for item in attends:
            if item not in show_list:
                item.delete()
    return HttpResponseRedirect("/")
