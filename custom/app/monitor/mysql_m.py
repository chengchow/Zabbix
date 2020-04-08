# -*- coding: utf-8 -*-
"""
参数列表
    参数1                            -->      参数2
    端口                             -->      qps,tps,reads,writes,slow_queries,tmp_disk_tables,select_full_join_per_second, ......

参数描述:
    qps                              -->      平均每秒查询请求数(count/s)
    tps                              -->      平均每秒提交的修改(count/s)
    reads                            -->      平均每秒读请求数(count/s)
    writes                           -->      平均每秒写请求数(count/s)
    slow_queries                     -->      平均每秒的慢查询书(count/s)
    tmp_disk_tables                  -->      平均每秒创建磁盘临时表数量(count/s)
    select_full_join_per_second      -->      平均每秒执行full join的总量(count/s)
    ...                              -->      ...

标准输出: 浮点数, 字符
作者: zz
版本: v1.0.0

备注: 
    参数太多,不在列出，详细参考mysql下global status和global variables变量名称
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
from function import load_json_file, get_index, get_sec_index, get_initdata, get_diffdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

def main(**kwargs):
    ## 获取项目标签
    label = cfg.mysqlLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 获取关键列表
    keyList = get_index(jsonFile=curFile)

    ## 获取结果
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数. '
        )
    else:
        secKeyList = get_sec_index(
            jsonFile = curFile,
            arg1     = arg1
        )

        if keyList:
            if arg1 in keyList:
                secKeyList = get_sec_index(
                    jsonFile = curFile,
                    arg1     = arg1
                )
                if secKeyList:
                    if arg2 == 'qps' :
                        diffQ  = get_diffdata(
                            arg1    = arg1, 
                            arg2    = 'questions', 
                            curFile = curFile, 
                            preFile = preFile
                        )
                        diffTm = get_diffdata(
                            arg1    = arg1, 
                            arg2    = 'uptime',
                            curFile = curFile,
                            preFile = preFile
                        )
                        try:
                            result = round(diffQ / diffTm, 2)
                        except (ZeroDivisionError,TypeError):
                            result = 0.0
                            logging.warning(
                                '除数为零或获值失败: diffQ={}, diffTm = {}'.format(
                                diffQ, diffTm)
                            )
                    elif arg2 == 'tps' :
                        diffIn = get_diffdata(
                            arg1    = arg1, 
                            arg2    = 'com_insert', 
                            curFile = curFile, 
                            preFile = preFile
                        )
                        diffDe = get_diffdata(
                            arg1    = arg1, 
                            arg2    = 'com_delete', 
                            curFile = curFile, 
                            preFile = preFile
                        )
                        diffUp = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'com_update',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffRe = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'com_replace',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffTm = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'uptime',
                            curFile = curFile,
                            preFile = preFile
                        )
                        try:
                             result = round((diffIn + diffDe + diffUp + diffRe) / diffTm, 2)
                        except (ZeroDivisionError,TypeError) :
                             result = 0.0
                             logging.warning(
                                 '除数为零或获值失败: diffIn={}, diffDe={}, diffUp={}, diffRe={}, diffTm={}'.format(
                                 diffIn, diffDe, diffUp, diffRe, diffTm)
                             )
                    elif arg2 == 'reads' :
                        diffSl = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'com_select',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffQH = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'qcache_hits',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffTm = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'uptime',
                            curFile = curFile,
                            preFile = preFile
                        )
                        try:
                            result = round((diffSl + diffQH) / diffTm, 2)
                        except (ZeroDivisionError,TypeError):
                            result = 0.0
                            logging.warning(
                                '除数为零或获值失败: diffSl={}, diffQH={}, diffTm = {}'.format(
                                diffSl, diffQH, diffTm) 
                            )
                    elif arg2 == 'writes' :
                        diffIn = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'com_insert',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffDe = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'com_delete',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffUp = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'com_update',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffTm = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'uptime',
                            curFile = curFile,
                            preFile = preFile
                        )
                        try:
                            result = round((diffIn + diffDe + diffUp) / diffTm, 2)
                        except (ZeroDivisionError,TypeError) :
                            result = 0.0
                            logging.warning(
                                '除数为零或获值失败: diffIn={}, diffDe={}, diffUp={}, diffTm = {}'.format(
                                diffIn, diffDe, diffUp, diffTm)
                            )
                    elif arg2 == 'slow_queries':
                        diffSQ = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'slow_queries',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffTm = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'uptime',
                            curFile = curFile,
                            preFile = preFile
                        )
                        try:
                            result = round(diffSQ / diffTm, 2)
                        except (ZeroDivisionError,TypeError) :
                            result = 0.0
                            logging.warning(
                                '除数为零或获值失败: diffSQ={}, diffTm = {}'.format(
                                diffSQ, diffTm)
                            )
                    elif arg2 == 'tmp_disk_tables' :
                        diffCTDT = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'created_tmp_disk_tables',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffTm   = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'uptime',
                            curFile = curFile,
                            preFile = preFile
                        )
                        try:
                            result = round(diffCTDT / diffTm, 2)
                        except (ZeroDivisionError,TypeError) :
                            result = 0.0
                            logging.warning(
                                '除数为零或获值失败: diffCTDT={}, diffTm = {}'.format(
                                diffCTDT, diffTm)
                            )
                    elif arg2 == 'select_full_join_per_second':
                        diffSFJPS = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'select_full_join',
                            curFile = curFile,
                            preFile = preFile
                        )
                        diffTm    = get_diffdata(
                            arg1    = arg1,
                            arg2    = 'uptime',
                            curFile = curFile,
                            preFile = preFile
                        ) 
                        try:
                            result = round(diffSFJPS / diffTm, 2)
                        except (ZeroDivisionError,TypeError) :
                            result = 0.0
                            logging.warning(
                                '除数为零或获值失败: diffSFJPS={}, diffTm = {}'.format(
                                diffSFJPS, diffTm)
                            )
                    elif arg2 in secKeyList:
                        result = get_initdata(
                            arg1     = arg1,
                            arg2     = arg2,
                            jsonFile = curFile
                        )
                    else:
                        logging.error(
                            '参数2错误, 请查看帮助文档. 当前参数: arg2={}'.format(
                            arg2)
                        )
                        result = None
                else:
                    logging.error(
                        '参数1错误, 请查看帮助文档. 当前参数: arg1={} '.format(
                        arg1)
                    )
                    result = None
                return result

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())

