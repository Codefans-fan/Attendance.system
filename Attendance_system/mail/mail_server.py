from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

import smtplib


class mail_server():
    def __init__(self,smtp_host,smtp_port=25,smtp_user=None,smtp_pass=None,smtp_encryption=None):
        '''
            :param host: host or IP of SMTP server to connect to
            :param int port: SMTP port to connect to
            :param user: optional username to authenticate with
            :param password: optional password to authenticate with
            :param string encryption: optional, ``'ssl'`` | ``'starttls'``
        '''
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.smtp_encryption = smtp_encryption
    
    def test_smtp_connection(self):
        try:
            smtp = self.connect()
        except Exception as e:
            print(e)
        finally:
            if smtp:
                smtp.quit()
    
    def connect(self):
        """Returns a new SMTP connection to the give SMTP server, authenticated
           with ``user`` and ``password`` if provided, and encrypted as requested
           by the ``encryption`` parameter. 
        """
        if self.smtp_encryption == 'ssl':
            if not 'SMTP_SSL' in smtplib.__all__:
                print('''error: Server does not support SMTP-over-SSL. You could use STARTTLS instead. If SSL is needed, an upgrade to Python 2.6 on the server-side should do the trick.''')
            connection = smtplib.SMTP_SSL(self.smtp_host,self.smtp_host)
        else:
            connection = smtplib.SMTP(self.smtp_host,self.smtp_port)
        
        if self.smtp_encryption == 'starttls':
            connection.starttls()
            
        if self.smtp_user:
            connection.login(self.smtp_user.encode('utf_8'), self.smtp_pass.encode('utf_8'))
        return connection
        
    def build_email(self,email_from,email_to,subject,body,email_cc=None, email_bcc=None,subtype='pain',headers = None,attachments=None):
        '''
        :param string subtype:  optional mime subtype for the text body (usually 'plain' or 'html'),
                                must match the format of the ``body`` parameter. Default is 'plain',
                                making the content part of the mail "text/plain".
        '''
        assert email_from, "You must provide a sender address."
        
        headers = headers or {}
        if not email_cc: email_cc = []
        if not email_bcc: email_bcc = []
        if not body: body = u''
        
        email_text_part = MIMEText(body.encode('utf_8'), _subtype=subtype, _charset='utf_8')
        msg = MIMEMultipart()
        
        msg['Subject'] = subject.encode('utf_8')
        msg['From'] = email_from.encode('utf_8')
        msg['To'] = email_to.encode('utf_8')
        
        
        # Custom headers may override normal headers or provide additional ones
        for key, value in headers.items():
            msg[key.encode('utf_8')] = value.encode('uft_8')
            
        msg.attach(email_text_part)
        
        if attachments:
            for (fname, fcontent) in attachments:
                filename_rfc2047 = fname.encode('utf_8')
                part = MIMEBase('application', "octet-stream")

                # The default RFC2231 encoding of Message.add_header() works in Thunderbird but not GMail
                # so we fix it by using RFC2047 encoding for the filename instead.
                part.set_param('name', filename_rfc2047)
                part.add_header('Content-Disposition', 'attachment', filename=filename_rfc2047)

                part.set_payload(fcontent)
                encoders.encode_base64(part)
                msg.attach(part)
        return msg
        
        
    def send_mail(self, message):
        
        smtp_from = message['From']
        assert smtp_from, "You must provide a sender address." 
        try:
            smtp = self.connect()
            smtp.sendmail(smtp_from,message['To'],message.as_string())
        finally:
                if smtp is not None:
                    smtp.quit()
if __name__=='__main__':
    mailserver = mail_server('127.0.0.1')
    msg = mailserver.build_email('test<562867448@qq.com>', 'test@test.com', 'Hello', 'fuck you')
    mailserver.send_mail(msg)