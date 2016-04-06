from django.shortcuts import render

from django.http import HttpResponseRedirect
# Create your views here.
from models import holiday_cn

import httplib2
import time
import json
import datetime



def syc_holiday_from_baidu(req):
    http = httplib2.Http()
    timestamp = str(time.time()).replace('.','')
    data = {'query':datetime.datetime.now().strftime('%Y-%m'),'resource_id':'6018','ie':'utf8','oe':'gbk','cb':'op_aladdin_callback','co':'','format':'json','tn':'baidu','cb':'jQuery1102018497919710353017_'+str(timestamp),'t':str(timestamp),'_':str(timestamp)}
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?'
    for key,val in data.items():
        url += key +'=' + val +'&'
    resp, content = http.request(url)
    start_index =  content.find('(')
    end_index = content.rfind(')')
    try:
        if start_index and end_index:
            holiday_list = json.loads(content[start_index+1:end_index].decode('gbk'))['data'][0]['holiday']
            for item in holiday_list:
                if len(item['list']):
                    for day_holiday in item['list']:
                        res = holiday_cn.objects.filter(holiday_name=item['name'],day=day_holiday['date'])
                        if not res:
                            holiday_cn(holiday_name =item['name'],day=day_holiday['date']).save()
    except Exception as e:
        print e
    finally:
        return HttpResponseRedirect("/")