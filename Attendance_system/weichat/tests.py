from django.test import TestCase


import httplib
import json
import urllib

# Create your tests here.
def _weichat_msg():
     c = httplib.HTTPSConnection("qyapi.weixin.qq.com")
     c.request("GET", "/cgi-bin/gettoken?corpid=wx416865667552f10b&corpsecret=60gcQRI8S-1hbMSvqf5CzBnYKBk1O3qOTmPw9Lk37Rxm6bFYifoyu4Me-P5sd53G")
     response = c.getresponse()
     print response.status, response.reason
     data = response.read()
     result = json.loads(data)
 
     token= result.get('access_token')
     print token
     #send message
     #https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN
 
     str_1 = '''{
    "touser": "fky",
    "msgtype": "text",
    "agentid": 0,
    "text": {
        "content": "Thank you for you follow DSA Account, you will get the attendance message at 8pm."
    },
    "safe":"0"
     }'''
     url = "/cgi-bin/message/send?access_token="+token
 
     c.request("POST",url ,str_1)
     response = c.getresponse()
     data = response.read()
     #print data



if __name__=='__main__':
    _weichat_msg()
