# -*- coding: utf-8 -*-
"""
参数列表:
    参数1               -->   参数2
    分区名称            -->   total,used,free,percent

参数描述:
    total               -->   当前分区总大小(bytes)
    used                -->   当前分区已经使用大小(bytes)
    free                -->   当前分区未使用大小(bytes)
    percent             -->   当前分区已经使用百分比(100%)

输出格式: 整数，浮点数
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
from monitor import cfg,socketTimeout

## 从全局函数文件中引用相应函数
from function import get_index, get_sec_index, get_initdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

def main(**kwargs):
    ## 获取监控项标识
    label = cfg.partitionLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)

    ## 获取关键词列表
    keyList = get_index(jsonFile = curFile)

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数'
        )
    else:
        secKeyList = get_sec_index(jsonFile = curFile, arg1 = arg1)

        if keyList and secKeyList:
            if arg1 in keyList and arg2 in secKeyList:
                result = get_initdata(
                    jsonFile = curFile,
                    arg1     = arg1,
                    arg2     = arg2
                )
                return result
            else:
                logging.error(
                    '参数错误, 当前参数: arg2={}'.format(arg2)
                )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
