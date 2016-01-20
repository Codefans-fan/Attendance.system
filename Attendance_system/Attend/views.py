from django.shortcuts import render

# Create your views here.

from models import Attend

def index(req):
    attends =  Attend.objects.filter(userId=1)
    
    return render(req, "Attend/index.html",context={'lines':attends})