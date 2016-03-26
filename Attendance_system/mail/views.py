from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from models import mailconfig
from django.contrib.auth.models import User

from models import EmailEditForm


# Create your views here.

@login_required(login_url="/user/login")
def mail_index(req):
    if req.method == 'POST':
        form = EmailEditForm(data=req.POST)
        if form.is_valid():
            lines = mailconfig.objects.filter(userid=req.user.id)
            if not lines:
                current_user = User.objects.get(id=req.user.id)
                userObj = mailconfig(userid=current_user,umail=form.cleaned_data['umail'],mail_template=form.cleaned_data['mailtemplate'])
                userObj.save()
            return HttpResponseRedirect("/email")
    else:
        lines = mailconfig.objects.filter(userid=req.user.id)
        if lines:
            form = EmailEditForm(initial={'username': req.user.username,'umail':lines[0].umail,'mailtemplate':lines[0].mail_template},)
        else:
            form = EmailEditForm(initial={'username': req.user.username},)
    context = {
        'form':form,
        'errors':form.errors
        }
    return render(req, 'mail/mail_index.html',context=context)