# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于创建Redis缓存数据, 仅在CacheAuto设置为True时自动执行

依赖:
    配置文件: conf/udt.py
    python模块: Redis

其他:
    作者: zz
    版本: v4.0.0
"""

## 调用python模块
import os, sys, json, time, socket
import psutil
import redis
import logging

## 获取根目录并添加到全局路径变量中
nowPath  = os.path.dirname(os.path.abspath(__file__))
homePath = os.path.join(nowPath, '../../')
sys.path.append(homePath)

## 从全局变量文件中引用相应变量
from monitor import cfg, osCfg, socketTimeout

## 从全局函数文件中引用相应变量
from function import cache_exec, cache_file

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 规范运行格式
if len(sys.argv)>1 and __name__ == '__main__':
    print("Usage: python",__file__)
    print(__doc__)
    sys.exit(0)

## 当前时间
nowTime = time.time()

## 项目标识
label = cfg.redisLabel

## 获取redis状态信息
def rds_info(_conn):
    _port    = _conn.get('RedisPort')
    _host    = _conn.get('RedisHost')
    _passwd  = _conn.get('RedisPass')

    try:
        _rdsInfo  = redis.Redis(host=_host,port=_port,password=_passwd).info()
    except redis.exceptions.ConnectionError:
        logging.error(
            'redis连接错误: host={}, port={}, passwd=******'.format(
            _host, _port)
        )
    else:
        return _rdsInfo

## 程序部分
def main():
    ## redis连接信息(所有端口)
    rdsConn = osCfg.rdsConn
    
    ## 获取redis的索引(端口)列表和信息列表
    nameList = [ '{}'.format(x.get('RedisPort')) for x in rdsConn]
    dataList = [ rds_info(x) for x in rdsConn ]

    ## 汇总数据字典
    dataDict = dict(zip(nameList, dataList))

    ## 生成输出字典
    outputDict = {
        'unixtime' : nowTime,
        'type'     : label,
        'data'     : dataDict
    }

    ## 写入缓存文件
    if cache_exec(label = label) == True:
        cache_file(label = label, data = outputDict)

    ## 返回数据, 调试使用
    return outputDict

## 调试
if __name__ == '__main__':
    print(json.dumps(main()))
