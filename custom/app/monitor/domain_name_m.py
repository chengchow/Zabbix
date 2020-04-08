# -*- coding: utf-8 -*-
"""
参数列表:
    参数1                        -->          参数2
    expire                       -->          url
参数描述：
    url                          -->          www.baidu.com
标准输出:
    整数
用途:
    获取域名过期天数,仅支持python3
备注:
    需要模块: python-whois
"""

## 导入python模块
import os, sys, time, socket
import logging
import datetime, whois

## 获取根目录并添加到全局路径变量中
nowPath  = os.path.dirname(os.path.abspath(__file__))
homePath = os.path.join(nowPath, '../../')
sys.path.append(homePath)

## 从全局变量文件中引用相应变量
from monitor import cfg, osCfg, socketTimeout

## 从全局函数文件中引用相应函数
from function import load_json_file

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
            '参数错误, 需要两个参数. '
        )
    else:
        if arg1 == 'expire':
            try:
                expireDate = whois.whois(arg2).expiration_date[0]
            except TypeError:
                logging.error(
                    '域名错误或网络不稳定: arg2={}'.format(
                    arg2)
                )
            else:
                nowDate    = datetime.datetime.now()
                oddDays    = (expireDate - nowDate).days
                result     = int(oddDays)
                return result
        else:
            logging.error(
                '首个参数只能是"expire": arg1={}'.format(
                arg1)
            )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
