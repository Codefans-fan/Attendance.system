from django.shortcuts import render

# Create your views here.

from models import Attend

from base.models import Menu

def index(req):
    attends =  Attend.objects.filter(userId=1)
    menu = __createMenu()
    return render(req, "Attend/index.html",context={'menu':menu,'lines':attends})


def __createMenu():
    menu_1 = Menu('Attend')
    menu_1.addMenu('All','http://www.baidu.com')
    menu_1.addMenu('All','http://www.baidu.com')
    
    
    
    menu_2 = Menu('Test1')
    menu_2.addMenu('All','http://www.baidu.com')
    menu_2.addMenu('All','http://www.baidu.com')
    return (menu_1,menu_2)
    
    