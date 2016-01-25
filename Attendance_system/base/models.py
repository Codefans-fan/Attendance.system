from __future__ import unicode_literals

from django.db import models

# Create your models here.


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