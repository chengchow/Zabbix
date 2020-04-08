# -*- coding: utf-8 -*-
"""
参数列表:
    参数1              -->    参数2
    analyze            -->    proc5cpu,proc5mem

参数描述:
    proc5cpu            -->    cpu占用前5进程字典
    proc5mem            -->    内存占用前5的进程字典

输出格式: 整数,字符
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
from monitor import cfg, osCfg, socketTimeout

## 从全局函数文件中引用相应函数
from function import load_json_file, list_dict_top

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.processLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)

    ## 获取当前数据
    curDict = load_json_file(curFile)

    ## 获取状态列表
    try:
        statusList = curDict.get('data').get('status')
    except:
        logging.error(
            '获取状态列表失败: curFile={}'.format(
            curFile)
        )
        statusList = []

    if statusList:
        ## 获取结果数据
        try:
            arg1 = kwargs.get('arg1') or sys.argv[1].lower()
            arg2 = kwargs.get('arg2') or sys.argv[2].lower()
        except IndexError:
            logging.error(
                '参数错误, 需要两个参数'
            )
        else:
             if arg1 == 'analyze' and arg2 == 'proc5cpu':
                 result = list_dict_top(statusList, 'cpu_percent', 5)
             elif arg1 == 'analyze' and arg2 =='proc5mem':
                 result = list_dict_top(statusList, 'memory_percent', 5)
             else:
                 logging.error(
                     '参数错误, 当前参数: arg1={} ,arg2={}'.format(
                     arg1, arg2)
                 )
                 result = None
             return result
    else:
        logging.warning(
            'status列表取值失败, 缓存数据错误: curFile={}'.format(
            curFile)
        )


## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
