# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于创建Docker缓存数据, 仅在CacheAuto设置为True时自动执行
需要:
    shell脚本: docker/stats.sh
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
from function import cache_exec, cache_file, convert_bytes

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
label = cfg.dockerLabel

## 程序部分
def main():
    ## 获取shell脚本路径
    shell = osCfg.dockerShell

    ## 获取shell脚本数据
    shellData = os.popen('/bin/bash {}'.format(shell)).read().strip('\r\n').split()

    ## 获取数据索引列表
    indexList = [ x for x in shellData if shellData.index(x) % 8 == 0 ] 
    
    ## 生成数据列表
    dataList= [
        {
            'cpu'        : round(float(shellData[ shellData.index(x) + 1 ].replace('%','')), 2),
            'mem'        : round(float(shellData[ shellData.index(x) + 2 ].replace('%','')), 2),
            'netin'      : convert_bytes(shellData[ shellData.index(x) + 3 ], shellData[ shellData.index(x) + 4 ]),
            'netout'     : convert_bytes(shellData[ shellData.index(x) + 6 ], shellData[ shellData.index(x) + 7 ])
        } for x in indexList
    ]

    ## 生成数据字典
    dataDict = dict(
        zip(indexList, dataList)
    )

    ## 生成输出字典
    outputDict = {
        'unixtime' : nowTime, 
        'type'     : 'docker', 
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
