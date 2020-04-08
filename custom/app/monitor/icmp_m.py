# -*- coding: utf-8 -*-
"""
参数列表:
    参数1              -->     参数2
    icmp               -->     检测地址(例如: www.baidu.com, 127.0.0.1)

参数描述:
    True                -->     连接正常
    False               -->     连接不正常

输出格式: 整数或者字符
作者: zz
版本: v1.0.0
"""

## 导入python模块
import os, sys, time, socket, psutil
import logging

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

## 主程序
def main(**kwargs):
    ## 判断命令参数
    if psutil.LINUX == True :
        args = ' -c 1 -W 1' 
    elif pstuil.WINDOWS == True :
        args = ' -n 1 -w 1'

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
             '参数错误, 需要两个参数. '
        )
    else:
        if arg1 == 'icmp':
            cmd = "ping {} {} > /dev/null 2>&1".format(arg2, args)
            result = os.system(cmd)
            if result == 0 :
                return True
            else:
                return False
        else:
            logging.error(
                '第一个参数只能是"icmd" : arg1={}'.formart(
                 arg1)
            )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())

