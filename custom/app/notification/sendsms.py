#! /usr/bin/python
#coding:utf-8
"""
该脚本用于短信通知
"""
import urllib2
import urllib
import sys

def sendm(mobile,content):
        url='http://************:****/sms-swagger/sms/sendSmsMessageYunwei?'
        data = urllib.urlencode({"toMobile":mobile,"message":content})
        req = urllib2.Request(url + data)
        res = urllib2.urlopen(req)
        print res.read()

number=sys.argv[1]
msg=sys.argv[2]
sendm(number,msg)
