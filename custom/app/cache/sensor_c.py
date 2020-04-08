# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于创建传感器缓存数据, 仅在CacheAuto设置为True时自动执行

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
from monitor import cfg, socketTimeout

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
label = cfg.sensorLabel

## 程序部分
def main():
    ### 温度信息
    tempInfo = hasattr(psutil, "sensors_temperatures") and psutil.sensors_temperatures()
    ### 温度索引列表
    nameList = [ x for x in tempInfo.keys() if tempInfo ]
    ### 温度数据列表
    tempList = [ [ psutil_to_dict(y) for y in x ] for x in tempInfo.values() if tempInfo ]
    ### 温度字典
    tempDict =dict(zip(nameList, tempList))

    ### 风扇转速信息
    fansInfo = hasattr(psutil, "sensors_fans") and psutil.sensors_fans()
    ### 风扇转速索引列表
    nameList = [ x for x in fansInfo.keys() if fansInfo ]
    ### 风扇转速数据列表
    fansList = [ [ psutil_to_dict(y) for y in x ] for x in fansInfo.values() if fansInfo ]
    ### 风扇转速字典
    fansDict = dict(zip(nameList, fansList))

    ## 数据字典
    dataDict = {
        'temperatures' : tempDict,
        'fans'         : fansDict
    }

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
