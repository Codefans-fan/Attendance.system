from django.shortcuts import render

# Create your views here.

def index(req):
    userInfo = req.session.get('userInfo',None)
    return render(req, 'base/index.html',{'userInfo':userInfo})


def base(req):
    return render(req,'base/base.html')