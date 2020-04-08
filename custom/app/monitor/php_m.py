# -*- coding: utf-8 -*-
"""
参数列表:
    参数1                   -->      参数2
    status                  -->      pool,process_manager,start_time,start_since,accepted_conn,listen_queue,max_listen_queue,
                                     listen_queue_len,idle_processes,active_processes,total_processes,max_active_processes,
                                     max_children_reached

参数描述:
    pool                    -->      fpm池子名称, 大多数为www(string)
    process_manager         -->      进程管理方式, 值: static, dynamic, ondemand(string)
    start_time              -->      启动日期, 如果reload了php-fpm, 时间会更新(date)
    start_since             -->      运行时长(seconds)
    accepted_conn           -->      当前池子接受的请求数(count/s)
    listen_queue            -->      请求等待队列, 如果这个值不为0, 那么要增加FPM的进程数量(count)
    max_listen_queue        -->      请求等待队列最高的数量(count)
    listen_queue_len        -->      socket等待队列长度(count)
    idle_processes          -->      空闲进程数量(count)
    active_processes        -->      活跃进程数量(count)
    total_processes         -->      总进程数量(count)
    max_active_processes    -->      最大的活跃进程数量(FPM启动开始算, count)
    max_children_reached    -->      进程最大数量限制的次数, 如果这个数量不为0, 那说明你的最大进程数量太小了, 需要设置大点(count)

输出格式: 字符, 浮点
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
from function import get_index, get_sec_index, get_initdata, get_avgdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.phpLabel

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
            '参数错误, 需要两个参数'
        )
    else:
        secKeyList = get_sec_index(
            jsonFile = curFile,
            arg1     = arg1
        )

        if keyList and secKeyList:
            if arg1 in keyList:
                if arg2 == 'accepted_conn':
                    result = get_avgdata(
                        curFile = curFile,
                        preFile = preFile,
                        arg1    = arg1,
                        arg2    = arg2
                    )
                    try:
                        return round(float(result), 2)
                    except TypeError:
                        return result
                elif arg2 in secKeyList:
                    result = get_initdata(
                        jsonFile = curFile,
                        arg1     = arg1,
                        arg2     = arg2
                    )
                    return result
                else:
                    logging.error(
                        '参数2错误, 当前参数: arg2={}'.format(
                        arg2)
                    )
            else:
                logging.error(
                    '参数1错误, 当前参数: arg1={}'.format(
                    arg1)
                )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
