# -*- coding: utf-8 -*-
"""
说明: 用于发现需要监控进程名称
输出: json格式
用途: zabbix自动发现
作者: zz
版本: v1.1.0
"""

## 调用python模块
import os,sys,json,socket

## 获取根目录并添加到全局路径变量中
nowPath  = os.path.dirname(os.path.abspath(__file__))
homePath = os.path.join(nowPath, '../../')
sys.path.append(homePath) 

## 从全局变量文件中引用相应变量
from monitor import osCfg, socketTimeout

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 规范运行格式
if len(sys.argv) > 1 and __name__ == '__main__' :
    print("Usage: python", __file__)
    print(__doc__)
    sys.exit(0)

## 关键词信息
keyInfo = osCfg.procList

##主程序
def main():
    ## 生成数据列表
    dataList = [
        { 
            '{#PROCESS_NAME}' : x,
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
