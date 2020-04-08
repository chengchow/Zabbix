# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于创建Nginx缓存数据, 仅在CacheAuto设置为True时自动执行

依赖:
    配置文件: conf/udt.py 

其他:
    作者: zz
    版本: v4.0.0
"""

## 调用python模块
import os, sys, json, time, socket
import psutil
import re
import urllib.request
import logging

## 获取根目录并添加到全局路径变量中
nowPath  = os.path.dirname(os.path.abspath(__file__))
homePath = os.path.join(nowPath, '../../')
sys.path.append(homePath)

## 从全局变量文件中引用相应变量
from monitor import cfg, osCfg, socketTimeout

## 从全局函数文件中引用相应变量
from function import cache_exec, cache_file, psutil_to_dict

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 规范运行格式
if len(sys.argv)>1 and __name__ == '__main__':
    print("Usage: python",__file__)
    print(__doc__)
    sys.exit(0)

## 指定日志格式
cfg.logFormat

## 当前时间
nowTime = time.time()

## 项目标识
label = cfg.nginxLabel

## 根据nginx status地址获取数据并列表输出
def get_url(_nginxUrl):
    try:
        _request = urllib.request.Request(_nginxUrl)
        _re      = urllib.request.urlopen(_request)
        _url     = _re.read().decode('utf-8')
    except urllib.error.URLError:
        logging.error(
            'url连接被拒绝: url={}'.format(
            _nginxUrl)
        )
    else:
        ## 提取url数据, 并转成列表格式
        _list = re.sub(r'\D', ' ', _url, count = 0 ,flags = 0).strip(' ').split()

        return _list

## 程序部分
def main():
    ## 获取nginx状态url地址和nginx状态列表
    ngxUrl = osCfg.ngxUrl
    ngxKeyList = osCfg.ngxKeyList

    ## 获取数据列表
    statsList = get_url(ngxUrl)

    ## 生成数据字典
    if statsList and ngxKeyList:
        statusDict = dict(zip(ngxKeyList, statsList))
    else:
        statusDict = {}

    ## 生成数据字典
    dataDict = {
        'status' : statusDict
    }
   
    ## 生成输出字典
    result = {
        'unixtime' : nowTime,
        'type'     : label,
        'data'     : dataDict
    }

    ## 写入缓存文件
    if cache_exec(label = label) == True:
        cache_file(label = label, data = result)

    ## 返回数据, 调试使用
    return result

## 调试
if __name__ == '__main__':
    print(json.dumps(main()))
