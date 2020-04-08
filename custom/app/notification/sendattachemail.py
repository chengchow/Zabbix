#!/usr/bin/python
#coding:utf-8 
"""
该脚本用于有附件邮件通知,
"""
import sys
import re
import smtplib
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
#from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
#from email.mime.multipart import MIMEMultipart  
#from email.mime.text import MIMEText  
#from email.mime.image import MIMEImage 

#邮件标题和内容
ToMail  = sys.argv[1]
Subject = sys.argv[2]
Message = sys.argv[3]
AttachPath="/data/software/zabbix/user_defined/cache/error_logs"

#发送邮件的相关信息，根据你实际情况填写
SmtpHost = 'smtp.uenpay.com'
FromMail = 'it.operations@uenpay.com'
UserName = 'it.operations@uenpay.com'
PassWord = 'Abcd@2020'

#定义smtp传输类型
SmtpType = 'ssl'    # smtp,tls,ssl

if SmtpType == 'ssl' :
    SmtpPort=465
else :
    SmtpPort=25

#设置默认字符集为UTF8 不然有些时候转码会出问题
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
 
#初始化邮件
Encoding = 'utf-8'
mail = MIMEMultipart('related')
msg = MIMEText(Message.encode(Encoding),'plain',Encoding)

mail.attach(msg)

mail['Subject'] = Header(Subject,Encoding)
mail['From'] = FromMail
mail['To'] = ToMail
mail['Date'] = formatdate()

TaskName=Subject.split(r'(')[2].split(')')[0]

AttachFile=AttachPath+"/"+TaskName+".cache"
FileName=TaskName + ".doc"
att = MIMEText(open(AttachFile,'rb').read(),'base64','utf-8')
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename=%s' % FileName.encode('utf-8')

mail.attach(att)

try:
	if SmtpType == 'ssl' :
		Smtp = smtplib.SMTP_SSL(SmtpHost,SmtpPort)
		Smtp.set_debuglevel(False)
		Smtp.ehlo()
		Smtp.login(UserName,PassWord)
	else :
		Smtp = smtplib.SMTP(SmtpHost,SmtpPort)
		Smtp.set_debuglevel(False)
	
		if SmtpType == 'tls' :
			Smtp.ehlo()
			Smtp.starttls()
			Smtp.ehlo()
	
		Smtp.login(UserName,PassWord)
	
	Smtp.sendmail(FromMail,ToMail,mail.as_string())
	Smtp.close()
except Exception as e:
	print e
