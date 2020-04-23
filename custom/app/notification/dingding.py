#!/usr/bin/python
#coding:utf-8
"""
该脚本获取与网络, 用于钉钉预警.
"""
import requests,json,sys,os,datetime
webhook="https://oapi.dingtalk.com/robot/send?access_token=65071be042d675f56ff535ee86bbd301bf64f**********dad6be5ce063d9297"
user=sys.argv[1]
text=sys.argv[3]
data={
    "msgtype": "text",
    "text": {
        "content": text
    },
    "at": {
        "atMobiles": [
            user
        ],
        "isAtAll": False
    }
}
headers = {'Content-Type': 'application/json'}
x=requests.post(url=webhook,data=json.dumps(data),headers=headers)
if os.path.exists("/data/software/zabbix/var/logs/dingding.log"):
    f=open("/data/software/zabbix/var/logs/dingding.log","a+")
else:
    f=open("/data/software/zabbix/var/logs/dingding.log","w+")
f.write("\n"+"--"*30)
if x.json()["errcode"] == 0:
    f.write("\n"+str(datetime.datetime.now())+"    "+str(user)+"    "+"发送成功"+"\n"+str(text))
    f.close()
else:
    f.write("\n"+str(datetime.datetime.now()) + "    " + str(user) + "    " + "发送失败" + "\n" + str(text))
    f.close(5)
