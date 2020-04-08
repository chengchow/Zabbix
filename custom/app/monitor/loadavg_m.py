# -*- coding: utf-8 -*-
"""
参数列表
    参数1            -->       参数2
    minutes          -->       1,5,15
参数描述:
    1                -->       1分钟内平均负载
    5                -->       5分钟内平均负载
    15               -->       15分钟内平均负载
标准输出: 浮点数
作者: zz
版本: v1.0.0
"""

## 导入python模块
import os, sys, time, socket
import logging
import psutil

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
    ## 定义loadavg列表
    minList = [1, 5, 15]

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数. '
        )
    else:
        if arg1 == 'minutes' and int(arg2) in minList:
            index  = minList.index(int(arg2))
            result = float(psutil.getloadavg()[index])
            return result
        else:
            logging.error(
                '第一个参数只能是minutes, 第二个参数只能在列表{}中, 当前参数是: arg1={}, arg2={}'.format(
                minList, arg1, arg2)
            )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
