# -*- coding: utf-8 -*-
"""
参数列表:
    参数1           -->     参数2
    virtual         -->     total,available,percent,used,free,active,inactive,buffers,cached,shared,slab
    swap            -->     total,used,free,percent,sin,sout

参数描述:
    total           -->     总(物理/虚拟)内存大小(bytes)
    available       -->     可用的内存大小(bytes)
    percent         -->     当前使用(物理/虚拟)内存百分比(%)
    used            -->     使用的(物理/虚拟)内存大小(bytes)
    free            -->     完全没有使用的(物理/虚拟)内存大小(bytes)
    active          -->     当前正在使用的物理内存(bytes)
    inactive        -->     标记为未使用的内存(bytes)
    buffers         -->     缓存文件系统元数据使用的内存(bytes)
    cached          -->     缓存各种文件的内存(bytes)
    shared          -->     可以被多个进程同时访问的内存(bytes)
    slab            -->     内核数据结构缓存的内存(bytes)

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
from function import get_index, get_sec_index, get_initdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.memoryLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)

    ## 关键词列表
    keyList    = get_index(jsonFile=curFile)

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
            jsonFile = curFile,
            arg1     = arg1
        )

        if keyList and secKeyList:
            if arg1 in keyList and arg2 in secKeyList:
                result = get_initdata(
                    arg1     = arg1,
                    arg2     = arg2,
                    jsonFile = curFile
                )
                return result
            else: 
                logging.error(
                    '参数错误, 请查看帮助文档: arg1={} arg2={}'.format(
                    arg1, arg2)
                )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
