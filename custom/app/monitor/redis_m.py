# -*- coding: utf-8 -*-
"""
参数列表:
    参数1         -->   参数2
    端口号        -->   qps,hit_rate,......

参数描述:
    qps           -->   每秒请求数(count/s)
    hit_rate      -->   查询命中率(%)
    ...

输出格式: 字符，浮点
作者: zz
版本: v1.0.0

备注: 
    参数太多，详细请查看redis-cli info中变量名称, 
    如上, 仅列出不在该列表中参数.
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
from function import get_index, get_sec_index, get_initdata, get_diffdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

def main(**kwargs):
    ## 获取监控项标识
    label = cfg.redisLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 关键词列表
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
        ) or []

        if arg1 in keyList:
            if arg2 == 'qps':
                diffQuestions = get_diffdata(
                     curFile = curFile,
                     preFile = preFile,
                     arg1    = arg1,
                     arg2    = 'total_commands_processed'
                )
                diffUptimes = get_diffdata(
                     curFile = curFile,
                     preFile = preFile,
                     arg1    = arg1,
                     arg2    = 'uptime_in_seconds'
                )
                try:
                    result = round(diffQuestions / diffUptimes, 2)
                except ZeroDivisionError:
                    result = 0.0
                    logging.warning(
                        '除数为零: diffUptimes={}'.format(
                        diffUptimes)
                    )
            elif arg2 == 'hit_rate':
                keyspaceHits   = float(get_initdata(jsonFile = curFile, arg1 = arg1, arg2 = 'keyspace_hits'))
                keyspaceMisses = float(get_initdata(jsonFile = curFile, arg1 = arg1, arg2 = 'keyspace_misses'))
                if keyspaceHits > 0 or keyspaceMisses > 0:
                    result = round(keyspaceHits * 100 / ( keyspaceHits + keyspaceMisses ), 2)
                else:
                    result = 0.0
                    logging.info(
                        '命中率为零: hits={}, misses={}'.format(
                        keyspaceHits, keyspaceMisses)
                    )
            elif arg2 in secKeyList:
                result = get_initdata(jsonFile = curFile, arg1 = arg1, arg2 = arg2)
            else:
                logging.error(
                    '参数2错误, 当前参数2: arg2={}'.format(
                    arg2)
                )
                result = None
            return result
        else:
            logging.error(
                '参数1错误, 当前参数1: arg1={}'.format(
                arg1)
            )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
