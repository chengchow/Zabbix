# -*- coding: utf-8 -*-

"""
说    明: 监控系统唯一调用接口,
配置范例: UserParameter=monitor[*],/data/software/zabbix/custom/run.py $1 $2 $3
作    者: zz
version : v4.0.0
用    法:
Usage: python run.py arg1 arg2 arg3
1. arg1为项目识别标签.
2. arg2, arg3为监控脚本对应参数
3. 发现脚本: python run.py auto find arg3
4. 监控脚本: python run.py arg1 arg2 arg3
"""

## 调用python模块
import os, sys, socket, time
import psutil
import logging

## 获取根路径, 并添加到全局路径变量中
nowPath  = os.path.dirname(os.path.abspath(__file__))
homePath = nowPath
sys.path.append(homePath)

## 从全局变量中引用相应变量
from monitor import cfg, osCfg, cacheTime, socketTimeout

## 从全局函数中引用相应函数
from function import cache_file, cache_exec

## 设置脚本socket超时时间
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 发现脚本调用函数
def exec_find(_label):
    ## 获取自动查找脚本路径
    _findPath = cfg.findAppPath
    ## 获取自动查找脚本名称
    _pyName ='{}_f'.format(_label)

    ## 将自动查找脚本追加到全局路径变量中
    sys.path.append(_findPath)

    ## 调用自动发现模块命令
    _importCmd = 'from {0} import {1} as {0}'.format(_pyName, 'main')
    ## 输出自动发现数据命令
    _moduleCmd = 'print({}())'.format(_pyName)

    ## 执行命令
    exec(_importCmd)
    exec(_moduleCmd)

## 缓存脚本调用函数
def exec_cache(_label):
    ## 获取缓存脚本路径
    _cachePath = cfg.cacheAppPath
    ## 缓存脚本名称
    _pyName='{}_c'.format(_label)   

    ## 将缓存脚本追加到全局路径变量中
    sys.path.append(_cachePath)

    ## 调用缓存模块命令
    _importCmd = 'from {0} import {1} as {0}'.format(_pyName, 'main')
    ## 输出自动发现数据命令
    _moduleCmd = '{}()'.format(_pyName)

    ## 执行命令
    exec(_importCmd)
    exec(_moduleCmd)

## 监控脚本调用函数
def exec_monitor(_label, _arg1, _arg2):
    ## 获取监控脚本路径
    _monitorPath = cfg.monitorAppPath

    ## 缓存脚本名称
    _pyName='{}_m'.format(_label)

    ## 将缓存脚本追加到全局路径变量中
    sys.path.append(_monitorPath)

    ## 执行命令
    _importCmd = 'from {0} import {1} as {0}'.format(_pyName, 'main')

    ## 输出自动发现数据命令
    _moduleCmd = "print({}(arg1='{}', arg2='{}'))".format(_pyName, _arg1, _arg2)

    exec(_importCmd)
    exec(_moduleCmd)

## 主程序
## 规范脚本参数数量
try:
    arg1, arg2, arg3 = sys.argv[1].lower(), sys.argv[2].lower(), sys.argv[3].lower()
except IndexError:
    logging.error(
        '参数错误, 需要三个参数.'
    )
else:
    ## 自动发现脚本调用
    if arg1 == 'auto' and arg2 =='find':
        try:
            exec_find(arg3)
        except ModuleNotFoundError:
            logging.warning(
                '不存在项目{}的自动发现脚本'.format(
                arg3)
            )
    else:
        ## 缓存脚本调用
        if arg1 in cfg.cacheProjList:
            ## 项目标签修正, 进程多项目公用一个缓存脚本
            try:
                if arg1 == 'proc_analyze' or arg1 == 'proc_exist' or arg1 == 'proc_status' :
                    if cache_exec(label = 'process') == True:
                        exec_cache('process')
                else:
                    if cache_exec(label = arg1) == True:
                        exec_cache(arg1)
            except ModuleNotFoundError:
                logging.info(
                    '项目{}不存在缓存或者缓存脚本不存在'.format(
                    arg1)
                )

        ## 监控脚本调用
        try:
            exec_monitor(arg1, arg2, arg3)
        except ModuleNotFoundError:
            logging.error(
                '项目数据获取失败: label(arg1)={}, arg1(arg2)={}, arg2(arg3)={}'.format(
                arg1, arg2, arg3)
            )
