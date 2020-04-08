# -*- coding: utf-8 -*-
"""
参数列表:
    参数1          -->    参数2
    磁盘名称       -->    read_count,write_count,read_bytes,write_bytes,read_time,write_time,read_merged_count,write_merged_count,busy_time

参数描述:
    read_count             -->   读取次数(count/s)
    write_count            -->   写入次数(count/s)
    read_bytes             -->   读取字节(bytes/s)
    write_bytes            -->   写入字节(bytes/s)
    read_time              -->   读取时间(ms/s)
    write_time             -->   写入时间(ms/s)
    read_merged_count      -->   读取合并次数(count/s)
    write_merged_count     -->   写入合并次数(count/s)
    busy_time              -->   忙碌时间(ms/s)

标准输出: 浮点数,
备注: 输出值为最近几分钟内平均每秒值.
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
from monitor import cfg, socketTimeout

## 从全局函数文件中引用相应函数
from function import get_index, get_sec_index, get_avgdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

def main(**kwargs):
    ## 获取项目标签
    label = cfg.diskioLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 获取磁盘列表
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
            jsonFile = curFile,
            arg1     = arg1
        )

        if keyList and secKeyList:
            if arg2 in secKeyList:
                result = get_avgdata(
                    arg1    = arg1,
                    arg2    = arg2,
                    curFile = curFile,
                    preFile = preFile
                )
                return result
            else:
                logging.error(
                    '参数2错误, 当前参数: arg2={}'.format(
                    arg2)
                )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
