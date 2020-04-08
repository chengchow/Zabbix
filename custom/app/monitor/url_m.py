# -*- coding: utf-8 -*-
"""
参数列表:
    参数1              -->     参数2
    http               -->     检测地址(例如: www.baidu.com)
    https              -->     检测地址(例如: news.sohu.com/?spm=smpc.home.top-nav.1.1564642374927Rjs3jFL)

参数描述:
    OK                 -->     正常
    其他               -->     不正常

输出格式: 字符
作者: zz
版本: v1.0.0
"""

## 导入python模块
import os, sys, time, socket
import logging

## 获取根目录并添加到全局路径变量中
nowPath  = os.path.dirname(os.path.abspath(__file__))
homePath = os.path.join(nowPath, '../../')
sys.path.append(homePath)

## 从全局变量文件中引用相应变量
from monitor import cfg,socketTimeout

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

def main(**kwargs):
    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数'
        )
    else:
        ## python2或者3的url请求
        _url = '{}://{}'.format(arg1, arg2)
        if sys.version[:1] == str(3):
            import ssl,urllib.request
            ssl._create_default_https_context = ssl._create_unverified_context
            try:
                request = urllib.request.Request(_url)
                re      = urllib.request.urlopen(request)
                url     = re.read().decode('utf-8')
                return True
            except Exception as e:
                return False
        elif sys.version[:1] == str(2):
            import ssl,urllib2
            try:
                ssl._create_default_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
        
            try:
                request = urllib2.Request(_url)
                re      = urllib2.urlopen(request)
                url     = re.read().decode('utf-8')
                return True
            except Exception as e:
                return False
       
## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
