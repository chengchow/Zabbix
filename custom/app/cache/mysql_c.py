# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于创建Mysql缓存数据, 仅在CacheAuto设置为True时自动执行

依赖:
    python模块: pymysql
    配置文件: conf/udt.py

其他:
    作者: zz
    版本: v4.0.0
"""


## 调用python模块
import os, sys, json, time, socket
import psutil
import pymysql
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

## 规范运行格式
if len(sys.argv)>1 and __name__ == '__main__':
    print("Usage: python",__file__)
    print(__doc__)
    sys.exit(0)

## 当前时间
nowTime = time.time()

## 项目标识
label = cfg.mysqlLabel

## 指定日志格式
cfg.logFormat

# mysql查询
def mysql_query(**kwargs):
    _cmd      = kwargs.get('cmd')
    _host     = kwargs.get('host')
    _user     = kwargs.get('user')
    _passwd   = kwargs.get('passwd')
    _port     = kwargs.get('port')
    _charset  = kwargs.get('charset')
    try:
        _db = pymysql.connect(
            host        = _host,
            user        = _user,
            passwd      = _passwd,
            port        = _port,
            charset     = _charset,
            cursorclass = pymysql.cursors.DictCursor
        )
    except Exception as e:
        logging.error("DB 连接失败: host={},user={},passwd='*******',port={},".format(
                       _host, _user, _port))
        logging.error(e)
        _result = []
    else:
        _cursor = _db.cursor()
        try:
            _cursor.execute(_cmd)
        except Exception as e:
            logging.error("SQL: {} 执行失败: ".format(_cmd))
            logging.error(e)
        else:
            _result = _cursor.fetchall()
            _cursor.close()
        _db.close()

    return _result

## 获取数据库的全局变量和全局状态信息
def data_query(_conn):
    _host    = _conn.get('MysqlHost')
    _user    = _conn.get('MysqlUser')
    _passwd  = _conn.get('MysqlPass')
    _port    = _conn.get('MysqlPort')
    _charset = 'utf8'

    _variablesInfo = mysql_query(
        cmd='show global variables', 
        host=_host, 
        user=_user, 
        passwd=_passwd, 
        port=_port, 
        charset=_charset
    )

    _statusInfo = mysql_query(
        cmd='show global status', 
        host=_host, 
        user=_user, 
        passwd=_passwd, 
        port=_port, 
        charset=_charset
    )

    ## 追加主从转态数据获取
    try:
        _slaveList = mysql_query(
            cmd='show slave status',
            host=_host,
            user=_user,
            passwd=_passwd,
            port=_port,
            charset=_charset
        )

        _slaveInfo=[ {'Variable_name': y, 'Value': z} for x in _slaveList for y,z in x.items()]

    except:
        _slaveInfo=[]


    _dataInfo = _variablesInfo + _statusInfo + _slaveInfo

    _dataIndex = [ x.get('Variable_name').lower() for x in _dataInfo ]
    _dataValue = [ x.get('Value') for x in _dataInfo ]

    _result=dict(zip(_dataIndex, _dataValue))

    return _result

## 程序部分
def main():
    ## 获取数据库连接信息
    mysqlConn = osCfg.mysqlConn
    ## 获取数据字典
    indexList = [ x.get('MysqlPort') for x in mysqlConn ]
    valueList = [ data_query(x) for x in mysqlConn ]

    dataDict = dict(zip(indexList, valueList))

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
