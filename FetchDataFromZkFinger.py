# -*- coding: utf-8 -*-
'''
Created on Feb 23, 2016

@author: fky
'''

#default password  dsa
# pbkdf2_sha256$20000$1OTf0NQKYUGm$/74pobT4hcILlod3RX+XqVQ4dCMVpUeTpHeIgsIjnbo=

from win32com.client import Dispatch

class AttLogsSys():
    def __init__(self,comName,m_ip,m_port,m_machin=1):
        self.manage = Dispatch("zkemkeeper.ZKEM")
        self.ip = m_ip
        self.port=m_port
        self.machine = m_machin
        
    def connect(self):
        if self.manage.Connect_Net(self.ip, self.port):
            self.manage.RegEvent(self.machine,65535)
            print 'connect success'
        else:
            print 'connect failed'
    
    def getAllUserInfo(self):
        '''
           get all User information
           return user list
                 (userid, username)
        '''
        userInfos = []
        self.manage.EnableDevice(self.machine, False)  #disable the device
        if self.manage.ReadAllUserID(self.machine):
            while True:
                data = self.manage.SSR_GetAllUserInfo(self.machine)
                if data[0]:
                    userInfos.append((data[1],data[2]))
                else:
                    break
        self.manage.EnableDevice(self.machine, True)  #enable the device
        return userInfos
    
    def getAllAttLogs(self):
        '''
           get all Attendance logs
           return att list
                 (userid, att_time)
        '''
        attList = []
        self.manage.EnableDevice(self.machine, False)  #disable the device
        if self.manage.ReadGeneralLogData(self.machine):
            while True:
                data = self.manage.SSR_GetGeneralLogData(self.machine)
                if data[0]:
                    attList.append((data[1],str(data[4])+'-'+str(data[5])+'-'+str(data[6])+' ' + str(data[7])+':'+str(data[8])+':'+str(data[9])))
                else:
                    break
        self.manage.EnableDevice(self.machine, True)  #enable the device
        return attList
    
    def disConnect(self):
        self.manage.Disconnect()
        
import psycopg2
def addUsersToPostgres(userList):
    conn = psycopg2.connect(database="attendance_system", user="odoo", password="odoo", host="172.69.8.148", port="5432")
    cur = conn.cursor()
    for item in userList:
        cur.execute("INSERT INTO auth_user(id,password,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)", (item[0],'pbkdf2_sha256$20000$1OTf0NQKYUGm$/74pobT4hcILlod3RX+XqVQ4dCMVpUeTpHeIgsIjnbo=',False,item[1],'','','',True,True,'2016-2-23 12:00:00'))
    conn.commit()
    cur.close()
    conn.close()

import datetime

def addAttLogsToPostgres(logList,isToday=None):
    conn = psycopg2.connect(database="attendance_system", user="odoo", password="odoo", host="172.69.8.148", port="5432")
    cur = conn.cursor()
    for item in logList:
        if isToday:
            now = datetime.datetime.now()
            today_str = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
            if(item[1] > today_str):
                cur.execute('''INSERT INTO "Attend_attend"(lock_time,comment,"userId_id") VALUES(%s, %s,%s)''', (item[1],'in',item[0]))
        else:
            cur.execute('''INSERT INTO "Attend_attend"(lock_time,comment,"userId_id") VALUES(%s, %s,%s)''', (item[1],'in',item[0]))
    conn.commit()
    cur.close()
    conn.close()

def RunOneTime():
    atts = AttLogsSys('zkemkeeper.ZKEM','172.69.8.4',4370)
    atts.connect()
    userList = atts.getAllUserInfo()
    atts.disConnect()
    addUsersToPostgres(userList)
    print 'run finish'

if __name__=='__main__':
    #RunOneTime()
    atts = AttLogsSys('zkemkeeper.ZKEM','172.69.8.4',4370)
    atts.connect()
    logList = atts.getAllAttLogs()
    atts.disConnect()
    addAttLogsToPostgres(logList)
    print 'run finish'




    
    