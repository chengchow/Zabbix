# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于创建DISKIO缓存数据, 仅在CacheAuto设置为True时自动执行
需要:
    python模块: psutil
信息:
    作者: zz
    版本: v4.0.0
"""

## 调用python模块
import os, sys, json, time, socket
import psutil

## 获取根目录并添加到全局路径变量中
nowPath  = os.path.dirname(os.path.abspath(__file__))
homePath = os.path.join(nowPath, '../../')
sys.path.append(homePath)

## 从全局变量文件中引用相应变量
from monitor import cfg, osCfg, socketTimeout

## 从全局函数文件中引用相应变量
from function import cache_exec, cache_file, psutil_to_dict

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 规范运行格式
if len(sys.argv)>1 and __name__ == '__main__' :
    print("Usage: python",__file__)
    print(__doc__)
    sys.exit(0)

## 当前时间
nowTime = time.time()

## 项目标识
label = cfg.diskioLabel

## 程序部分
def main():
    ## 获取索引列表
    keyList = osCfg.diskList

    ## 获取项目psutil数据
    psutilDataList = psutil.disk_io_counters(perdisk=True)

    ## 获取项目索引列表对应数据
    valueList = [ psutil_to_dict(psutilDataList.get(x)) for x in keyList ]

    ## 转置数据列表和索引数据为输出数据字典
    dataDict = dict(zip(keyList, valueList))

    ## 生成输出字典
    outputDict = {
        'unixtime' : nowTime, 
        'type'     : 'diskio', 
        'data'     : dataDict
    }

    ## 写入缓存文件
    if cache_exec(label = label) == True:
        cache_file(label = label, data = outputDict)

    ## 返回数据, 调试使用
    return outputDict

## 调试
if __name__ == '__main__':
    print(json.dumps(main()))
