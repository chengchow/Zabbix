# -*- coding: utf-8 -*-
"""
参数列表:
    参数1              -->     参数2
    login              -->     user

参数描述:
    user               -->     当前登录用户数(count)

输出格式: 整数
作者: zz
版本: v4.0.0
"""

## 导入python模块
import os, sys, time, socket
import psutil
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
        if arg1 == 'login' and arg2 == 'user':
            result = len(psutil.users())
            return result
        else:
            logging.error(
                '参数错误(Usage: python {} login user), 当前参数: arg1={}, arg2={}'.format(
                __file__, arg1, arg2)
            )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
