from django.shortcuts import render

# Create your views here.

def index(req):
    return render(req, 'base/index.html')


def base(req):
    return render(req,'base/base.html')