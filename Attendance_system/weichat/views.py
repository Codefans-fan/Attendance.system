from django.http import HttpResponseRedirect
from Attend.models import Attend
from models import user_weichat
from django.contrib.auth.models import User

import datetime
# Create your views here.
msg_templete = '''{
   "touser": "%s",
   "msgtype": "text",
   "agentid": 0,
   "text": {
       "content": "work hour: %d. (contain lunch time)"
   },
   "safe":"0"
    }'''


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
    token = _get_weichat_token()
    for user in users:
        ref_weichat = user_weichat.objects.filter(userid=user.id)
        if ref_weichat:
            attends =  Attend.objects.filter(userId=user.id,lock_time__gte = datetime.datetime.today().strftime("%Y-%m-%d")).order_by('lock_time')
            show_list = __filter_day_record(attends)
            if len(show_list) > 1:
                delta_time = show_list[-1].lock_time - show_list[0].lock_time
                msg_str = msg_templete %(ref_weichat[0].weichatname,int(delta_time))
                _weichat_msg(msg_str,token)
            else:
                msg_str = msg_templete %(ref_weichat[0].weichatname,0)
                _weichat_msg(msg_str,token)
    return HttpResponseRedirect("/")


import httplib
import json
import urllib


def _weichat_msg(msg,token):
    url = "/cgi-bin/message/send?access_token="+token
    c = httplib.HTTPSConnection("qyapi.weixin.qq.com")
    c.request("POST",url ,msg)
    response = c.getresponse()
    data = response.read()
    print data

def _get_weichat_token():
    c = httplib.HTTPSConnection("qyapi.weixin.qq.com")
    c.request("GET", "/cgi-bin/gettoken?corpid=wx416865667552f10b&corpsecret=60gcQRI8S-1hbMSvqf5CzBnYKBk1O3qOTmPw9Lk37Rxm6bFYifoyu4Me-P5sd53G")
    response = c.getresponse()
    #print response.status, response.reason
    data = response.read()
    result = json.loads(data)
    return result.get('access_token',False)

