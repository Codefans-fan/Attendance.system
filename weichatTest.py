

import httplib
import json
import urllib
#https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=id&corpsecret=secrect

#https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=wx416865667552f10b&corpsecret=1IJjmshb3HqhL-ryzwn_xw81zEWBCmLdrKYPgxMX56TBjkEXUA281wd8rbERuvi8



c = httplib.HTTPSConnection("qyapi.weixin.qq.com")
c.request("GET", "/cgi-bin/gettoken?corpid=xxxxxx&corpsecret=xxxxxx")
response = c.getresponse()
print response.status, response.reason
data = response.read()
result = json.loads(data)

token= result.get('access_token')
print token
#send message
#https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=ACCESS_TOKEN

params = urllib.urlencode({'touser': '@all','toparty':'@all','totag':'@all','msgtype': "text",'agentid':0,'text':{'content':'hello world'},'safe':'0'})
headers = {"Content-type": "application/x-www-form-urlencoded"
                    , "Accept": "text/plain"}
str_1 = '''{
   "touser": "fky",
   "msgtype": "text",
   "agentid": 0,
   "text": {
       "content": "Holiday Request For Pony(http://xxxxx)"
   },
   "safe":"0"
}'''
url = "/cgi-bin/message/send?access_token="+token

c.request("POST",url ,str_1)
response = c.getresponse()
data = response.read()
print data