from django.shortcuts import render

from models import Attend
from django.contrib.auth.models import User

import datetime
# Create your views here.
def task_weichat_notice(req):
    users = User.objects.all()
    for user in users:
        if user.id == 21:
            attends =  Attend.objects.filter(userId=user.id,lock_time__gte = datetime.datetime.today().strftime("%Y-%m-%d")).order_by('lock_time')
            show_list = __filter_day_record(attends)
            if len(show_list) > 1:
                delta_time = show_list[-1].lock_time - show_list[0].lock_time
                if delta_time >= datetime.timedelta(hours=9):
                    print 'lock success'
                else:
                    _weichat_msg()
            else:
                _weichat_msg()
    return HttpResponseRedirect("/")


import httplib
import json
import urllib

def _weichat_msg():
    c = httplib.HTTPSConnection("qyapi.weixin.qq.com")
    c.request("GET", "/cgi-bin/gettoken?corpid=wx416865667552f10b&corpsecret=60gcQRI8S-1hbMSvqf5CzBnYKBk1O3qOTmPw9Lk37Rxm6bFYifoyu4Me-P5sd53G")
    response = c.getresponse()
    #print response.status, response.reason
    data = response.read()
    result = json.loads(data)

    token= result.get('access_token')
    #print token
    #send message
    #https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN

    str_1 = '''{
   "touser": "@all",
   "msgtype": "text",
   "agentid": 0,
   "text": {
       "content": "Do not forget to lock out..."
   },
   "safe":"0"
    }'''
    url = "/cgi-bin/message/send?access_token="+token

    c.request("POST",url ,str_1)
    response = c.getresponse()
    data = response.read()
    #print data


