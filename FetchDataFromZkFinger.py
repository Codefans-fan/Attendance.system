 # -*- coding: utf-8 -*-
'''
Created on Feb 23, 2016

@author: fky
'''

#default password  dsa
# pbkdf2_sha256$20000$1OTf0NQKYUGm$/74pobT4hcILlod3RX+XqVQ4dCMVpUeTpHeIgsIjnbo=

from win32com.client import Dispatch

import logging  
import logging.handlers


LOG_FILE = 'fetchData.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # handler   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  

formatter = logging.Formatter(fmt)   # formatter  
handler.setFormatter(formatter)      # add formatter  

logger = logging.getLogger('fetch')    # get logger  
logger.addHandler(handler)           # add logger handler  
logger.setLevel(logging.DEBUG)  

class AttLogsSys():
    def __init__(self,comName,m_ip,m_port,m_machin=1):
        self.manage = Dispatch("zkemkeeper.ZKEM")
        self.ip = m_ip
        self.port=m_port
        self.machine = m_machin
        
    def connect(self):
        if self.manage.Connect_Net(self.ip, self.port):
            self.manage.RegEvent(self.machine,65535)
            logger.info('connect '+self.ip + 'success.')
        else:
            logger.info('connect '+self.ip + 'fail.')
    
    def getAllUserInfo(self):
        '''
           get all User information
           return user list
                 (userid, username)
        '''
        logger.info('start get user info.')
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
        logger.info('end get user info.')
        return userInfos
    
    def getAllAttLogs(self):
        '''
           get all Attendance logs
           return att list
                 (userid, att_time)
        '''
        logger.info('start get attendance log.')
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
        logger.info('end get attendance log.')
        return attList
    
    def disConnect(self):
        logger.info('disconnect the machine.')
        self.manage.Disconnect()
        
import psycopg2
def addUsersToPostgres(userList):
    logger.info('add/update user info to database.')
    try:
        conn = psycopg2.connect(database="xxxx", user="xxx", password="xxx", host="xxxx", port="5432")
        cur = conn.cursor()
        for item in userList:
            logger.info('check user ' + str(item[0]))
            #cur.execute("INSERT INTO auth_user(id,password,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)", (item[0],'pbkdf2_sha256$20000$1OTf0NQKYUGm$/74pobT4hcILlod3RX+XqVQ4dCMVpUeTpHeIgsIjnbo=',False,item[1],'','','',True,True,'2016-2-23 12:00:00'))
            #cur.execute("if not exists(select * from auth_user where id = %s) begin insert into auth_user(id,password,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined) VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s) end", (item[0],item[0],'pbkdf2_sha256$20000$1OTf0NQKYUGm$/74pobT4hcILlod3RX+XqVQ4dCMVpUeTpHeIgsIjnbo=',False,item[1],'','','',True,True,'2016-2-23 12:00:00'))
            cur.execute('SELECT update_userdb(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)', (item[0],'pbkdf2_sha256$20000$1OTf0NQKYUGm$/74pobT4hcILlod3RX+XqVQ4dCMVpUeTpHeIgsIjnbo=',False,item[1],'','','',True,True,'2016-2-23 12:00:00'))
        conn.commit()
        cur.close()
        conn.close()
    except e:
        logger.error(e)
    logger.info('end add/update user info to database.')

import datetime

def addAttLogsToPostgres(logList,isToday=None):
    logger.info('add attendance log to database.')
    try:
        conn = psycopg2.connect(database="xxxx", user="xxx", password="xxx", host="xxx", port="5432")
        cur = conn.cursor()
        for item in logList:
            if isToday:
                #now = datetime.datetime.now()
                #today_str = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
                today_str = '2016-03-16'
                if(item[1] > today_str):
                    #cur.execute('''INSERT INTO "Attend_attend"(lock_time,comment,"userId_id") VALUES(%s, %s,%s)''', (item[1],'in',item[0]))
                    cur.execute('''SELECT update_attendancedb(%s, %s)''',(item[0],item[1]))
            else:
                cur.execute('''INSERT INTO "Attend_attend"(lock_time,comment,"userId_id") VALUES(%s, %s,%s)''', (item[1],'in',item[0]))
        conn.commit()
        cur.close()
        conn.close()
    except e:
        logger.error(e)
    logger.info('end add attendance log to database.')

if __name__=='__main__':
    # RunOneTime()
#     logger.info('script start.')
#     atts = AttLogsSys('zkemkeeper.ZKEM','xxx',4370)
#     atts.connect()
#     userinfos = atts.getAllUserInfo()
#     #logList = atts.getAllAttLogs()
#     atts.disConnect()
#     #addUsersToPostgres(userinfos)
#     #addAttLogsToPostgres(logList,True)
#     print userinfos
    
    atts = AttLogsSys('zkemkeeper.ZKEM','172.69.8.5',4370)
    atts.connect()
    logList = atts.getAllAttLogs()
    atts.disConnect()
    addAttLogsToPostgres(logList,True)
     
    logger.info('script end.')


    
    