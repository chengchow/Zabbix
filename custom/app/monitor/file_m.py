# -*- coding: utf-8 -*-
"""
参数列表：
    参数1         -->    参数2
    files         -->    文件全路径
    dirs          -->    目录全路径
参数描述:
    False         -->    未变更
    True          -->    被修改
标准输出: 布尔值
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
from function import load_json_file, get_index, get_sec_index, get_initdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat


## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.fileLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 获取索引
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
        secKeyList = get_sec_index( jsonFile = curFile, arg1 = arg1)

        if keyList and secKeyList:
           if arg1 in keyList and arg2 in secKeyList:
               curValue = get_initdata(
                   arg1     = arg1,
                   arg2     = arg2,
                   jsonFile = curFile
               )
               preValue = get_initdata(
                   arg1     = arg1,
                   arg2     = arg2,
                   jsonFile = preFile
               )
               if curValue != None and preValue != None :
                   if curValue == preValue:
                       result = False
                   else:
                       result = True
               else:
                   logging.warning(
                       '当前值或之前值不存在: preValue={}, curValue={}, preFile={}, curFile'.format(
                       preValue, curValue, preFile, curFile)
                   )
                   result = None
           else:
               logging.error(
                   '参数错误: arg1={}, arg2={}, curFile={}, preFile={}'.format(
                   arg1, arg2, curFile, preFile)
               )
               result = None
           return result

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
