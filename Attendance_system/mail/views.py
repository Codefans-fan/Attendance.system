from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from models import mailconfig
from django.contrib.auth.models import User
from Attend.models import Attend

from models import EmailEditForm

import mail_server


import datetime
# Create your views here.

MAIL_TEMPLATE = 'work hours: %s. (contain lunch time)'

@login_required(login_url="/user/login")
def mail_index(req):
    if req.method == 'POST':
        form = EmailEditForm(data=req.POST)
        if form.is_valid():
            lines = mailconfig.objects.filter(userid=req.user.id)
            if not lines:
                current_user = User.objects.get(id=req.user.id)
                user_obj = mailconfig(userid=current_user,umail=form.cleaned_data['umail'],mail_template=form.cleaned_data['mailtemplate'])
                user_obj.save()
            else:
                lines[0].umail = form.cleaned_data['umail']
                lines[0].mail_template=form.cleaned_data['mailtemplate']
                lines[0].save()
            return HttpResponseRedirect("/notice")
    else:
        lines = mailconfig.objects.filter(userid=req.user.id)
        if lines:
            form = EmailEditForm(initial={'username': req.user.username,'umail':lines[0].umail,'mailtemplate':MAIL_TEMPLATE},)
        else:
            form = EmailEditForm(initial={'username': req.user.username},)
    context = {
        'form':form,
        'errors':form.errors
        }
    return render(req, 'mail/mail_index.html',context=context)


def __filter_day_record(records):
    if records:
        res = []
        days_group =[list(group) for k, group in itertools.groupby(records,key=lambda args: args.lock_time.day)]
        for grp in days_group:
            grp.sort(key=lambda p: p.lock_time)
            if len(grp) > 1:
                res.append(grp[0])
                res.append(grp[-1])
            else:
                res.append(grp[0])
        return res
    return []
    

def task_mail_notice(req):
    users = User.objects.all()
    for user in users:
        umail_obj = mailconfig.objects.filter(userid=user.id)
        if umail_obj:
            attends =  Attend.objects.filter(userId=user.id,lock_time__gte = datetime.datetime.today().strftime("%Y-%m-%d")).order_by('lock_time')
            show_list = __filter_day_record(attends)
            if len(show_list) > 1:
                delta_time = show_list[-1].lock_time - show_list[0].lock_time
                work_hour = float('%.2f' % (delta_time.total_seconds()/3600))
                if work_hour < 9.0:
                    msg_str = umail_obj[0].mail_template % work_hour
                    mailserver = mail_server.mail_server('127.0.0.1')
                    msg = mailserver.build_email('test<562867448@qq.com>', umail_obj[0].umail, 'Work Hours', msg_str)
                    mailserver.send_mail(msg)
            else:
                msg_str = umail_obj[0].mail_template % 0
                mailserver = mail_server.mail_server('127.0.0.1')
                msg = mailserver.build_email('test<562867448@qq.com>', umail_obj[0].umail, 'Work Hours', msg_str)
                mailserver.send_mail(msg)
    return HttpResponseRedirect("/")


    