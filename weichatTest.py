

import httplib
import json
import urllib
#https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=id&corpsecret=secrect

#https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=wx416865667552f10b&corpsecret=1IJjmshb3HqhL-ryzwn_xw81zEWBCmLdrKYPgxMX56TBjkEXUA281wd8rbERuvi8



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

# get user id
#https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=ACCESS_TOKEN&userid=USERID
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


url1 = '/cgi-bin/user/get?access_token=' + token +'&userid=fky'
c.request("POST",url ,str_1)
response = c.getresponse()
data = response.read()
print data