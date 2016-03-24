from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/user/login")
def mail_index(req):
    return render(req, 'mail/mail_index.html')