# -*- coding: utf-8 -*-
"""
说明: 用于发现需要监控端口信息，需要在udt.py中配置
输出: json格式
用途: zabbix自动发现
作者: zz
版本: v1.1.0
"""

## 调用python模块
import os
import sys
import json
import socket

## 获取根目录并添加到全局路径变量中
homePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
sys.path.append(homePath) 

## 从全局变量文件中引用相应变量
from monitor import osCfg
from monitor import socketTimeout

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 规范运行格式
if len(sys.argv) > 1 and __name__ == '__main__' :
    print("Usage: python", __file__)
    print(__doc__)
    sys.exit(0)

## 关键词信息
keyInfo = osCfg.logKeys

##主程序
def main():
    ## 生成数据列表
    dataList = [
        { 
            '{#SIGN}'   : x.get('sign'),
            '{#NAME}'   : x.get('name'),
            '{#KEYWORD}'   : x.get('keyword'),
            '{#LOGDIR}' : x.get('logdir'),
            '{#DOUBLETHORLD}' : x.get('doublethorld'),
        } for x in keyInfo
    ]
    
    ## 生成输出字典
    outputDict = {
        'data' : dataList
    }
    
    ## 转数组格式为json字符串
    outputStr = json.dumps(
        outputDict, 
        ensure_ascii = False
    )
    
    ## 返回数据
    return outputStr

## 调试
if __name__ == '__main__':
    print(main())
