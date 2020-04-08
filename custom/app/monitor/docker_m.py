# -*- coding: utf-8 -*-
"""
参数列表:
    参数1         -->    参数2
    all           -->    list,number
    docker名称    -->    cpu,mem

参数描述:
    list          -->    当前所有活跃pod列表
    num           -->    当前活跃pod数量
    cpu           -->    对应pod cpu百分比(%)
    mem           -->    对应pod mem百分比(%)
    netin         -->    对应pod 网卡流量(入)
    netout        -->    对应pod 网卡流量(出)


标准输出: 浮点数,字符
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
from function import load_json_file, get_index, get_initdata, get_avgdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.dockerLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 获取关键词列表
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
        if arg1 == 'all' and arg2 == 'list':
            result  = keyList
        elif arg1 == 'all' and arg2 == 'number':
            result  = len(keyList)
        elif arg1 in keyList and arg2 in ('cpu', 'mem'):
            result  = get_initdata(
                arg1     = arg1,
                arg2     = arg2,
                jsonFile = curFile
            )
        elif arg1 in keyList and arg2 in ('netin', 'netout'):
            result = get_avgdata(
                arg1    = arg1,
                arg2    = arg2,
                curFile = curFile,
                preFile = preFile
            )
        else:
            logging.error(
                '参数不正确，请查看文档, arg1 = {}, arg2 = {}'.format(
                arg1, arg2)
            )
            result = None

        return result

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
