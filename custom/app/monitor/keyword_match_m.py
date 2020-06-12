# -*- coding: utf-8 -*-
"""
参数列表:
    参数1              -->     参数2
    logkeys            -->     项目sign

参数描述:
    Yes                -->     日志匹配到关键词
    No                 -->     日志没有匹配到关键词
    Unkown             -->     出现未知因素
    None               -->     查看自定义日志

输出格式: 布尔值或字符串
作者: zz
版本: v4.0.0
"""

## 导入python模块
import os
import sys
import time
import socket
import logging

## 获取根目录并添加到全局路径变量中
homePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
sys.path.append(homePath)

## 从全局变量文件中引用相应变量
from monitor import cfg
from monitor import osCfg
from monitor import socketTimeout

## 从全局函数文件中引用相应函数
from function import load_json_file

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.keywordMatchLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 获取当前数据和之前数据
    curInfo = load_json_file(curFile)
    preInfo = load_json_file(preFile)

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数'
        )
    else:
        ## 统计日志文件触发次数在当前文件和A, 当前文件和之前文件同时出现的之前文件触发次数B
        ## 如果A-B大于0, 返回Yes(触发); 等于0, 返回No(不触发); 小于0, 返回Unkown(管理员触发)
        if curInfo and preInfo:
            try:
                ## 从当前缓存文件获取日志关键词项目索引
                projList = [ x for x in curInfo.get('data')]
            except Exception as e:
                logging.error(
                    '当前缓存文件缺失数据. curFile={}'.format(
                    curFile, preFile))
            else:
                if arg1 == 'logkeys' and arg2 in projList:
                    ## 获取当前数据和之前数据
                    curData = curInfo.get('data').get(arg2)
                    preData = preInfo.get('data').get(arg2)

                    ## 当前触发次数和之前触发次数和
                    curTotal = sum(map(lambda x:x[1], curData))
                    preTotal = sum(x[1] for x in preData if x[0] in map(lambda y:y[0], curData))

                    ## 两次获取之间关键词次数差值
                    re = curTotal - preTotal

                    return re
#                    ## 判断返回值
#                    if re > 0:
#                        return 'Yes'
#                    elif re == 0:
#                        return 'No'
#                    else:
#                        return 'Unkown'
                else:
                    logging.error(
                        '参数错误. 当前参数是arg1={}, arg2={}'.format(
                            arg1, arg2)
                         )
        else:
            logging.error(
                '当前缓存文件或之前缓存文件不存在. curFile={}, preFile={}'.format(
                    curFile, preFile)
                )


## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
