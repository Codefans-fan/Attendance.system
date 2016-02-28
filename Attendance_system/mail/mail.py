# -*- coding: utf-8 -*-
'''
Created on Feb 29, 2016

@author: fky
'''

import smtplib
from email.utils import parseaddr, formataddr
from email import encoders
from email.header import Header
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage 
# smtp


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))
class  mail():
    def __init__(self,m_user, m_pass):
        self._umail = m_user
        self._upass = m_pass
        self.smtp_server = None
        self.smtp_server_name = None
        self.smtp_port = None
        self.content = None
        self.subject = None
        self.msg = MIMEMultipart('related')
        self.recvs= []   # mail_to list
        self.type = 'text'   # msg type, default is text
        self.isLogin = False
    def set_smtp_server(self,m_server,m_port=25):
        self.smtp_server_name = m_server
        self.smtp_port = m_port
        self.smtp_server = smtplib.SMTP(m_server, m_port) 
        
    
    def set_content(self,m_content):
        self.content = m_content
#         if self.recvs:
#             self.content = MIMEText(m_content, 'plain', 'utf-8')
#             self.content['From'] =  self._umail
#         else:
#             print 'please set the recvs first.'
#             exit(1)
    def set_msg_type(self,m_type='text'):
        self.type = m_type
    def set_recvs(self,mail_list):
        ''' email list  '''
        self.recvs.extend(mail_list)
        
    def set_subject(self,subject):
        self.subject = subject
    
    def add_image(self,image_path,imgid):
        fp = open(image_path, 'rb')  
        msgImage = MIMEImage(fp.read())  
        fp.close()  
        self.msg.add_header('Content-ID', imgid)  
        self.msg.attach(msgImage)  
    
    
    def add_attach(self,filepath):
        att = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')  
        att["Content-Type"] = 'application/octet-stream'  
        att["Content-Disposition"] = 'attachment; filename="1.jpg"'  
        self.msg.attach(att)
    
    def send_mail(self,from_mail=None,mail_password=None):
        if from_mail:
            pass  # send by different user
        else:
            if not self.isLogin:
                self._login_server()
            self._format_msg()
            self.smtp_server.sendmail(self._umail, self.recvs, self.msg.as_string())
    
    def _format_msg(self):
        self.msg.attach(MIMEText(self.content, self.type, 'utf-8'))
        self.msg['Subject'] = self.subject
#         self.msg['From'] = self._umail
#         self.msg['To'] = self.recvs
        
    def _login_server(self):
        self.smtp_server.login(self._umail,self._upass)
        self.isLogin = True
    
    def exit_server(self):
        self.smtp_server.quit()
    

if __name__=='__main__':
    test_mail = mail('fankeyuan1990@163.com','fankeyuan520520')
    test_mail.set_smtp_server('smtp.163.com')
    test_mail.set_recvs(['562867448@qq.com',])
    test_mail.set_msg_type('html')
    test_mail.set_content('<b>Some <i>HTML</i> text</b>')
    test_mail.set_subject('fuck you')
    #test_mail.add_image(test.png, 'test')
    test_mail.send_mail()
    test_mail.exit_server()
