from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

from models import Attend

from base.models import Menu
from base.models import BaseManu

@login_required(login_url="/user/login")
def index(req):
    attends =  Attend.objects.filter(userId=req.user.id)
    menu = __createMenu(req.user)
    basemenu = []
    basemenu.append(__createMainMenu())
    context = {
        'basemenu':basemenu,
        'menu':menu,
        'lines':attends
        }
    
    return render(req, "Attend/index.html",context=context)

@login_required(login_url="/user/login")
def show_my_attendance(req, userid = None):
    if userid is None:
        attends = []
    elif userid == 'all':
        attends =  Attend.objects.filter()
    else:
        attends =  Attend.objects.filter(userId=userid)
    menu = __createMenu(req.user)
    basemenu = []
    basemenu.append(__createMainMenu())
    context = {
        'basemenu':basemenu,
        'menu':menu,
        'lines':attends
        }
    
    return render(req, "Attend/index.html",context=context)

def __createMenu(user):
    menu_1 = Menu('Attend')
    menu_1.addMenu('My attendance','id='+str(user.id))
    menu_1.addMenu('All','id=all')
    
    
    
    return (menu_1,)
    
def __createMainMenu():
    mainMenu = BaseManu('Attend','/attend')
    return mainMenu