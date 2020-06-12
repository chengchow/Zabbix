# -*- coding: utf-8 -*-
"""
参数列表:
    参数1                     -->     参数2
    项目名称                  -->     (threadcount,heapmemoryusage,nonheapmemoryusage,codecache,oldgen,edenspace,survivorspace,metaspace,
                                       compressedclassspace,classcount,openfiledescriptorcount,maxfiledescriptorcount,cpuusage)

参数描述:
    threadcount               -->     线程(子进程)数                        (count)
    heapmemoryusage           -->     堆内存使用情况                        (bytes)
    nonheapmemoryusage        -->     非堆内存使用情况                      (bytes)
    codecache                 -->     内存池: "Code Cache"                  (bytes)
    oldgen                    -->     内存池: "PS Old Gen"                  (bytes)
    edenspace                 -->     内存池: "PS Eden Space"               (bytes)
    survivorspace             -->     内存池: "PS Survivor Space"           (bytes)
    metaspace                 -->     内存池: "Meta Space"                  (bytes)
    compressedclassspace      -->     内存池: "Compressed Class Space"      (bytes)
    classcount                -->     已加载类数量                          (count)
    openfiledescriptorcount   -->     打开文件描述符数                      (count)
    maxfiledescriptorcount    -->     最大打开文件描述符数                  (count)
    cpuusage                  -->     cpu使用百分比                         (%)

输出格式: 整数,浮点数
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
from function import load_json_file, get_initdata, get_index, get_sec_index

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.jmxLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 获取项目列表
    keyList = get_index(jsonFile=curFile)

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
            if arg1 in keyList and arg2 == 'cpuusage':
                cpuCount = get_initdata(
                    arg1     = arg1,
                    arg2     = 'availableprocessors',
                    jsonFile = curFile
                )
                curTime  = get_initdata(
                    arg1     = arg1,
                    arg2     = 'uptime',
                    jsonFile = curFile
                )
                preTime  = get_initdata(
                    arg1     = arg1,
                    arg2     = 'uptime',
                    jsonFile = preFile
                )
                curProcTime  = get_initdata(
                    arg1     = arg1,
                    arg2     = 'processcputime',
                    jsonFile = curFile
                )
                preProcTime  = get_initdata(
                    arg1     = arg1,
                    arg2     = 'processcputime',
                    jsonFile = preFile
                )
    
                if curTime and preTime and curProcTime and preProcTime:
                    diffTime     = float(curTime) - float(preTime)
                    diffProcTime = float(curProcTime) - float(preProcTime)
                    try:
                        result = round(diffProcTime * 100 / diffTime/ cpuCount, 2 )
                        return result
                    except ZeroDivisionError:
                        result = 0.0
                        logging.warning(
                            '除数为零: diffTime = {}, cpuCount={}'.format(
                            diffTime, cpuCount)
                        )
            elif arg1 in keyList and arg2 in secKeyList:
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
