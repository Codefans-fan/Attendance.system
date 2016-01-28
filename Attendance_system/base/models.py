from django.db import models

# Create your models here.
import json

# base class 
# menu

class Menu():
    def __init__(self, topName):
        self.topName = topName
        
        self.subMenus = []
    def addMenu(self, title, url):
        self.subMenus.append((title,url))
        
    def get_topName(self):
        return self.topName
    
    def get_subMenus(self):
        return self.subMenus
    
class BaseManu():
    def __init__(self,displayName,url):
        self.display = displayName
        self.url = url
from datetime import datetime
from datetime import date     
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)