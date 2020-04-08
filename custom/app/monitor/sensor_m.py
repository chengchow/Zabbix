# -*- coding: utf-8 -*-
"""
参数列表：
    参数1                -->    参数2
    temperatures         -->    coretemp ...
    fans                 -->    cpufans ...

参数描述:
    coretemp             -->    cpu单核最高温度
    cpufans              -->    cpu最高风扇转速

标准输出: 浮点数,整数, 字符
作者: zz
版本: v1.0.0

备注: 
    输出0为不支持,虚拟机温度输出值是100.

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

## 从全局函数文件中引用相应函数
from function import load_json_file

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

def main(**kwargs):
    ## 获取监控项标识
    label = cfg.sensorLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)

    ## 获取数据
    curDict = load_json_file(curFile)

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数'
        )
    else:
        if arg1 == 'temperatures' or arg1 == 'fans':
            try:
                _dict = curDict.get('data').get(arg1).get(arg2)
            except:
                logging.error(
                    '获取温度字典失败, 请检测数据文件: curFile={}'.format(
                    curFile)
                )
            else:
                if _dict:
                    _list = [ float(x.get('current')) for x in _dict ]
                    result = max(_list)
                    return result
                else:
                    logging.info(
                         '传感器不支持该选项: arg1={}, arg2={}'.format(
                         arg1, arg2)
                    )
                    return 0.0

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
