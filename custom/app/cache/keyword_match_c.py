# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于日志关键词匹配, 仅在cacheType设置为True时执行
需求:
    :
其他:
    作者: zz
    版本: v4.0.0
备注:
    如果日志文件过大, 会导致脚本执行时间超过Zabbix脚本运行时间限制，建议采用多进程模式调用.
"""

## 调用python模块
import os
import sys
import json
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

## 从全局函数文件中引用相应变量
from function import cache_exec
from function import cache_file
from function import load_json_file

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 当前时间
nowTime = time.time()

## 项目标识
label = cfg.keywordMatchLabel

## 获取上传缓存数据文件信息
jsonPath = os.path.join(cfg.cachePath, label)
curJsonFile = os.path.join(jsonPath, cfg.curCache.format(label))

cacheFileInfo = load_json_file(curJsonFile)

## 获取截取日志的时间差
if cacheFileInfo:
    diffTime = abs(cacheFileInfo.get('unixtime')-time.time())
#    diffTime = 360000    
else:
    diffTime = 120

## 转置时间YYYY-MM-DD HH:MM:SS格式为unix时间
def time_convert(dateTime):
    timeArray = time.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
    unixTime = time.mktime(timeArray)

    return unixTime

## 获取当日日志文件列表, 按照修改时间逆序排序
## 如果日志文件夹创建了新的文件或者日志被修改，会导致数据出错
def get_file_list(projInfoDict):
    ## 获取日志路径
    logDir = projInfoDict.get('logdir').format(
        year = time.strftime("%Y", time.localtime()),
        mon  = time.strftime("%m", time.localtime()),
        date = time.strftime("%d", time.localtime())
    )

    ## 获取日志文件列表    
    try:
        logFile = os.listdir(logDir)
    except FileNotFoundError:
        ## 跨日期可能导致出错
        time.sleep(1)
        logFile = os.listdir(logDir)

    ## 获取文件时间元组组合
    fileTime = ((x, os.path.getmtime(os.path.join(logDir, x))) for x in logFile)

    ## 文件时间元组排序按照时间逆序
    fileTimeSort = sorted(fileTime, key=lambda x:x[1], reverse=True)

    ## 获取按照时间逆序全路径文件组合
    result = map(lambda x:os.path.join(logDir, x[0]), fileTimeSort)

    ## 返回数据
    return tuple(result)


## 轮询查询逆序列表中的文件, 如果文件开始时间大于设置触发时间, 删除后面的文件
def modify_file_list(fileList, diffTime):
    ## 创建初始输出列表
    reList = []

    ## 轮询所有日志文件, 找出在二次获取数据时间内内的日志文件。
    for _file in list(fileList):
        with open(_file, 'r') as f:
            try:
                firstLine = f.readline()
            except UnicodeDecodeError:
                logging.error(
                    '编码错误, 文件被打开或者存在非utf8编码. file={}'.format(
                    _file))

            try:
                lineTime = int(time_convert(str(firstLine).split(',')[0]))
            except TypeError:
                logging.error(
                    '数据类型错误. number={}'.format(
                    str(firstLine).split(',')[0]))
            else:
                reList.append(_file)
                if nowTime-lineTime > diffTime:
                    break
    ## 返回数据
    return reList

## 统计日志文件关键词出现次数
def get_keyword_count(logFile, keyword):
    with open(logFile) as f:
        info = f.readlines()
        count = str(info).count(keyword)

    return count

## 汇总日志列表中文件关键词出现次数, 以[(文件名称, 次数), ...]格式输出
def get_keyword_total(fileList, keyword):
    re = list(map(lambda x:(os.path.basename(x), get_keyword_count(x, keyword)), fileList))

    return re

## 主程序/调用函数
def main():
    ## 获取日志配置信息
    logKeys = osCfg.logKeys

    ## 获取日志项目列表
    keyList = map(lambda x:x.get('sign'), logKeys)

    ## 获取日志关键词触发次数列表
    countList = map(lambda x:get_keyword_total(modify_file_list(get_file_list(x), diffTime), x.get('keyword')), logKeys)

    ## 转置日志项目和日志关键词次数数组
    reList = dict(zip(keyList, countList))

    ## 生成输出字典
    outputDict = {
        'unixtime' : nowTime,
        'type'     : label,
        'data'     : reList
    }

    ## 写入缓存文件
    if cache_exec(label = label) == True:
        cache_file(label = label, data = outputDict)

    ## 返回数据, 调试使用
    return outputDict

# 调试
if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False))
