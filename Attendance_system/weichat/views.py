from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from Attend.models import Attend
from models import user_weichat
from django.contrib.auth.models import User

from models import WechatEditForm

import datetime
import itertools
import wechat_utils
# Create your views here.

@login_required(login_url="/user/login")
def weichat(req):
    if req.method == 'POST':
        form = WechatEditForm(data=req.POST)
        if form.is_valid():
            lines = user_weichat.objects.filter(userid=req.user.id)
            if not lines:
                current_user = User.objects.get(id=req.user.id)
                userObj = user_weichat(userid=current_user,weichatname=form.cleaned_data['shortname'])
                userObj.save()
            return HttpResponseRedirect("/weichat")
    else:
        lines = user_weichat.objects.filter(userid=req.user.id)
        shortname =''
        if lines:
            shortname= lines[0].weichatname
        if shortname:
            form = WechatEditForm(readonly_shortname=True,initial={'username': req.user.username,'shortname':shortname},)
        else:
            form = WechatEditForm(initial={'username': req.user.username},)
    context = {
        'form':form,
        'errors':form.errors.get('shortname','')
        }
    return render(req, "weichat/weichat.html",context)

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
    

def task_weichat_notice(req):
    users = User.objects.all()
    token = wechat_utils.get_weichat_token()
    for user in users:
        ref_weichat = user_weichat.objects.filter(userid=user.id)
        if ref_weichat:
            attends =  Attend.objects.filter(userId=user.id,lock_time__gte = datetime.datetime.today().strftime("%Y-%m-%d")).order_by('lock_time')
            show_list = __filter_day_record(attends)
            if len(show_list) > 1:
                delta_time = show_list[-1].lock_time - show_list[0].lock_time
                work_hour = float('%.2f' % (delta_time.total_seconds()/3600))
                msg_str = wechat_utils.msg_templete %(ref_weichat[0].weichatname,work_hour)
                wechat_utils.weichat_msg(msg_str,token)
            else:
                msg_str = wechat_utils.msg_templete %(ref_weichat[0].weichatname,0)
                wechat_utils.weichat_msg(msg_str,token)
    return HttpResponseRedirect("/")