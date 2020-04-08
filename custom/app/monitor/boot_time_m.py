# -*- coding: utf-8 -*-
"""
参数列表:
    参数1                      -->          参数2
    boot                       -->          time
参数描述:
    time                       -->          启动时间(秒)
标准输出: 整数
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
from monitor import cfg, socketTimeout

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
        if arg1 == 'boot' and arg2 == 'time':
            bootTime = psutil.boot_time()
            nowTime  = time.time()
            result   = int(nowTime - bootTime)
            return result
        else:
            logging.error(
                '参数错误, 当前参数: arg1={}, arg2={}'.format(
                arg1, arg2)
            )
            pass

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
