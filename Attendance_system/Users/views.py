from django.shortcuts import render
from django.http import HttpResponseRedirect


from models import User

# Create your views here.
def login(req):
    if req.method == 'POST':
        userName =  req.POST.get('username','')
        passwd = req.POST.get('password','')
        user = User.objects.filter(name=userName, password = passwd)
        if user:
            # login success
            userInfo = {'UserID': user[0].id,
                        'UserName':user[0].name,}
            
            req.session['userInfo'] = userInfo
            return HttpResponseRedirect('/')
        else:
            return  HttpResponseRedirect('/user/login', {})
    else:
      
        return render(req, 'login.html', {})