# -*- coding: utf-8 -*-
"""
参数列表:
    参数1           -->    参数2
    exist           -->    进程名称(输出: 布尔值)

参数描述:
    True            -->    端口可以连接
    False           -->    端口不能连接

输出格式: 布尔值
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
from function import load_json_file

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

def main(**kwargs):
    ## 获取监控项标识
    label = cfg.processLabel

    ## 获取进程列表
    procList = osCfg.procList

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)

    ## 获取当前字典
    curDict = load_json_file(curFile)

    ## 获取结果数据
    try:
        procNameList = [ x.get('name') for x in curDict.get('data').get('status')]
    except:
        logging.warning(
            '获取进程名称列表失败: curFile = {}'.format(
            curFile)
        )
    else:
        try:
            arg1 = kwargs.get('arg1') or sys.argv[1].lower()
            arg2 = kwargs.get('arg2') or sys.argv[2].lower()
        except IndexError:
            logging.error(
                '参数错误, 需要两个参数'
            )
        else:
            if procNameList:
                if arg1 == 'exist':
                    if arg2 in procNameList:
                        return True
                    else:
                        return False
                else:
                    logging.error(
                        '参数1错误, 当前参数1: arg1={}'.format(
                        arg1)
                    )
            else:
                loggin.warning(
                    '进程列表为空, 请检测缓存文件: curFile={}'.format(
                    curFile)
                )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
