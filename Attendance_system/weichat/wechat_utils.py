# -*- coding: utf-8 -*-
'''
Created on Mar 22, 2016

@author: fky
'''

import httplib
import json
import urllib

msg_templete = '''{
   "touser": "%s",
   "msgtype": "text",
   "agentid": 0,
   "text": {
       "content": "work hour: %s (contain lunch time)"
   },
   "safe":"0"
    }'''


def weichat_msg(msg,token):
    url = "/cgi-bin/message/send?access_token="+token
    c = httplib.HTTPSConnection("qyapi.weixin.qq.com")
    c.request("POST",url ,msg)
    response = c.getresponse()
    data = response.read()
    c.close()

def get_weichat_token():
    c = httplib.HTTPSConnection("qyapi.weixin.qq.com")
    c.request("GET", "/cgi-bin/gettoken?corpid=wx416865667552f10b&corpsecret=60gcQRI8S-1hbMSvqf5CzBnYKBk1O3qOTmPw9Lk37Rxm6bFYifoyu4Me-P5sd53G")
    response = c.getresponse()
    #print response.status, response.reason
    data = response.read()
    result = json.loads(data)
    c.close()
    return result.get('access_token',False)

def validate_weichat_user(uname,token):
    c = httplib.HTTPSConnection("qyapi.weixin.qq.com")
    url = '/cgi-bin/user/get?access_token='+ token + '&userid='+uname
    c.request('GET', url)
    response = c.getresponse()
    data = response.read()
    result = json.loads(data)
    c.close()
    user_state = result.get('status',0)
    if user_state != 1:
        return False
    return True
