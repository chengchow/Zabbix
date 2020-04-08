# -*- coding: utf-8 -*-
"""
参数列表:
    参数1              -->     参数2
    tcp                -->     端口号(输出: 布尔值)

参数描述:
    True               -->     端口可以连接
    False              -->     端口不能连接

输出格式: 布尔值
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
from monitor import cfg, osCfg, socketTimeout

## 从全局函数文件中引用相应函数
from function import get_index, get_sec_index, get_initdata, get_avgdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取端口列表
    portList = osCfg.portList

    ## 获取发布标识位置
    thorldSheildFile = osCfg.thorldSheildFile

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数'
        )
    else:
        if os.path.isfile(thorldSheildFile):
            result = True                                                    ## 触发屏蔽文件存在不触发端口预警
        elif arg1 == 'tcp' or arg1 == 'exist':
            ipAddr = '127.0.0.1'
            for x in portList:
                if int(x.get('PortNumber')) == arg2:
                    ipAddr = x.get('HostAddr')
                    break
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((ipAddr, int(arg2)))
                sock.close
                result = True
            except socket.error:
                result = False
        else:
            logging.error(
                '参数错误, 当前参数: arg1={}'.format(
                arg1)
            )
            result = None
        return result

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
