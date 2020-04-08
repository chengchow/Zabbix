# -*- coding: utf-8 -*-
"""
参数列表:
    参数1                  -->          参数2
    网卡名称               -->          bytes_sent,bytes_recv,packets_sent,packets_recv,errin,errout,dropin,dripout

参数描述:
    bytes_sent             -->          发送的字节数(bytes/s)
    bytes_recv             -->          收到的字节数(bytes/s)
    packets_sent           -->          发送的数据包数量(count/s)
    packets_recv           -->          接收的数据包数量(count/s)
    errin                  -->          接收时的错误总数(count/s)
    errout                 -->          发送时的错误总数(count/s)
    dropin                 -->          丢弃的传入数据包总数(count/s)
    dropout                -->          丢弃的传出数据包总数(在OSX和BSD上始终为0, count/s)

标准输出: 浮点数
作者: zz
版本: v4.0.0
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
from function import get_index, get_sec_index, get_avgdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.trafficLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 获取网卡列表
    keyList = get_index(jsonFile = curFile)

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数. '
        )
    else:
        secKeyList = get_sec_index(
            arg1     = arg1,
            jsonFile = curFile
        )

        if keyList and secKeyList:
            if arg1 in keyList and arg2 in secKeyList:
                result = get_avgdata(
                    arg1    = arg1,
                    arg2    = arg2,
                    curFile = curFile,
                    preFile = preFile
                )
                return result
            else:
                logging.error(
                    '参数错误, 当前参数: arg1 = {}, arg2 = {}'.format(
                    arg1, arg2)
                )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())

