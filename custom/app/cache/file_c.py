# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于创建关键文件缓存数据, 仅在CacheAuto设置为True时自动执行
需要:
    配置文件: conf/files.py
信息:
    作者: zz
    版本: v4.0.0
"""

## 调用python模块
import os, sys, json, time, socket
import hashlib
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
label = cfg.fileLabel

## 指定日志格式
cfg.logFormat

## md5比较(需要文件只读权限权限, 误报率低)
def file_md5sum(_file):
    if os.path.isfile(_file):
        _myHash = hashlib.md5()
        try:
            _f = open(_file, 'rb')
        except PermissionError as e:
            logging.error('MD5检测文件需要只读权限: file={}'.format(_file))
            logging.error(e)
        else:
            while True:
                _b = _f.read(8096)
                if not _b :
                    break
                _myHash.update(_b)
            _f.close()
            return _myHash.hexdigest()
    else:
        logging.warning('文件不存在: file={}'.format(_file))

## 目录md5比较
def dir_md5sum(_dir):
    return ''.join(file_md5sum(os.path.join(_dir, _x)) for _x in os.listdir(_dir))

## 时间戳比较(不需要文件只读权限, 误报率高)
def file_mtime(_file):
    if os.path.isfile(_file):
        return os.stat(_file).st_mtime
    else:
        logging.warning('文件不存在: file={}'.format(_file))

## 目录时间戳比较
def dir_mtime(_dir):
    return sum(file_mtime(os.path.join(_dir, _x)) for _x in os.listdir(_dir))

## 程序部分
def main():
    ## 获取待检测文件列表和目录列表
    fileList = osCfg.fileList
    dirList  = osCfg.dirList

    ## 获取待检测文件列表和目录列表文件的修改时间戳或者MD5值(目录列表为该目录下所有文件值的汇总)
    ### fileDataList = [ file_md5sum(x) for x in fileList ]       ## MD5比较
    ### dirDataList  = [ dir_md5sum(x) for x in dirList ]         ## MD5比较
    fileDataList = [ file_mtime(x) for x in fileList ]        ## 时间戳比较
    dirDataList  = [ dir_mtime(x) for x in dirList ]          ## 时间戳比较

    ## 生成文件列表和目录列表的数据字典
    fileDict = dict(zip(fileList, fileDataList))
    dirDict  = dict(zip(dirList, dirDataList))

    ## 生成汇总数据字典
    dataDict = {
        'file' : fileDict,
        'dir'  : dirDict
    }

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
