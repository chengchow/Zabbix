# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于创建网卡流量缓存数据, 仅在CacheAuto设置为True时自动执行
依赖:
    python模块: psutil
其他:
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
if len(sys.argv)>1 and __name__ == '__main__':
    print("Usage: python",__file__)
    print(__doc__)
    sys.exit(0)

## 当前时间
nowTime = time.time()

## 项目标识
label = cfg.trafficLabel

## 程序部分
def main():
    ## 获取网络设配器列表
    netcardList = osCfg.netcardList

    ## 获取数据列表
    trafficList = [ psutil_to_dict(psutil.net_io_counters(pernic=True).get(x)) for x in netcardList ]

    ## 生成数据字典
    dataDict = dict(zip(netcardList, trafficList))

    ## 生成输出字典
    outputDict = {
        'unixtime' : nowTime,
        'type'     : label,
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
