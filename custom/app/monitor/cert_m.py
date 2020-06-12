# -*- coding: utf-8 -*-
"""
参数列表:
    参数1                      -->          参数2
    域名                       -->          端口
参数描述：
    域名                       -->          www.baidu.com
    端口                       -->          443
标准输出:
    整数
用途:
    获取证书过期天数,仅支持python3
备注:
    需要模块: pyOpenSSL,urllib3
"""

## 导入python模块
import os, sys, socket
from urllib3.contrib import pyopenssl as reqs
from datetime import datetime
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

## 程序部分
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
        try:
            X509 = reqs.OpenSSL.crypto.load_certificate(
                reqs.OpenSSL.crypto.FILETYPE_PEM, 
                reqs.ssl.get_server_certificate((arg1, arg2))
            )
        except Exception as e:
            logging.error(
            '连接超时，请检查域名, 端口和网络稳定性.'
        )
        else:
            expireDate = datetime.strptime(X509.get_notAfter().decode()[0:-1], '%Y%m%d%H%M%S')
            remainDays = expireDate - datetime.now()
            result     = int(remainDays.days)
            return result

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())

