#!/usr/bin/python
#coding:utf-8 
"""
该脚本用于一般邮件通知
"""
import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
import sys

#设置默认字符集为UTF8 不然有些时候转码会出问题
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
 
#发送邮件的相关信息，根据你实际情况填写
SmtpHost = 'smtp.exmail.qq.com'
FromMail = 'it.operations@uenpay.com'
UserName = 'it.operations@uenpay.com'
PassWord = 'Abcd@2020'

SmtpType = 'ssl'	# smtp,tls,ssl

if SmtpType == 'ssl' :
	SmtpPort=465
else :
	SmtpPort=25
  
#邮件标题和内容
ToMail	= sys.argv[1]
Subject	= sys.argv[2]
Message	= sys.argv[3]

#初始化邮件
Encoding = 'utf-8'
mail = MIMEText(Message.encode(Encoding),'plain',Encoding)
mail['Subject'] = Header(Subject,Encoding)
mail['From'] = FromMail
mail['To'] = ToMail
mail['Date'] = formatdate()

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
