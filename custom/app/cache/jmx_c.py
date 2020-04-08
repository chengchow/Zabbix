# -*- coding: utf-8 -*-
"""
说明: 
    该脚本用于创建CPU缓存数据, 仅在cacheType设置为True时执行
需求:
    python模块: psutil
其他:
    作者: zz
    版本: v4.0.0
"""

## 调用python模块
import os, sys, json, time, socket
import psutil
import jpype
from jpype import java, javax
import logging

## 获取根目录并添加到全局路径变量中
nowPath  = os.path.dirname(os.path.abspath(__file__))
homePath = os.path.join(nowPath, '../../')
sys.path.append(homePath)

## 从全局变量文件中引用相应变量
from monitor import cfg, osCfg, socketTimeout

## 从全局函数文件中引用相应变量
from function import cache_exec, cache_file, psutil_to_dict

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
label = cfg.jmxLabel

## java项目监控信息输出
def proj_info(**kwargs):
    _host   = kwargs.get('host')   or '127.0.0.1'
    _port   = kwargs.get('port')
    _user   = kwargs.get('user')   or ''
    _passwd = kwargs.get('passwd') or ''

    _dict = {}

    _connUrl = "service:jmx:rmi:///jndi/rmi://%s:%d/jmxrmi" % (_host, _port)

    _jhash  = java.util.HashMap()
    _jarray = jpype.JArray(java.lang.String)([_user, _passwd])
    _jhash.put (javax.management.remote.JMXConnector.CREDENTIALS, _jarray);
    _jmxurl = javax.management.remote.JMXServiceURL(_connUrl)
    try:
        _jmxsoc = javax.management.remote.JMXConnectorFactory.connect(_jmxurl, _jhash)
    except:
        logging.error(
            'JMX连接被拒绝: url={}'.format(
            _jmxurl)
        )
    else:
        _conn   = _jmxsoc.getMBeanServerConnection();
    
        ## 堆内存
        _object                          = "java.lang:type=Memory"
        _attribute                       = "HeapMemoryUsage"
        _dict['heapmemoryusage']         = _conn.getAttribute(javax.management.ObjectName(_object),_attribute).get('used')
    
        ## 非堆内存
        _object                          = "java.lang:type=Memory"
        _attribute                       = "NonHeapMemoryUsage"
        _dict['nonheapmemoryusage']      = _conn.getAttribute(javax.management.ObjectName(_object),_attribute).get('used')
    
        ## 内存池Code Cache
        _object                          = "java.lang:type=MemoryPool,name=Code Cache"
        _attribute                       = "Usage"
        _dict['codecache']               = _conn.getAttribute(javax.management.ObjectName(_object),_attribute).get('used')
    
        ## 内存池Old Gen
        _object                          = "java.lang:type=MemoryPool,name=PS Old Gen"
        _attribute                       = "Usage"
        _dict['oldgen']                  = _conn.getAttribute(javax.management.ObjectName(_object),_attribute).get('used')
    
        ## 内存池Eden Space
        _object                          = "java.lang:type=MemoryPool,name=PS Eden Space"
        _attribute                       = "Usage"
        _dict['edenspace']               = _conn.getAttribute(javax.management.ObjectName(_object),_attribute).get('used')
    
        ## 内存池Survivor Space
        _object                          = "java.lang:type=MemoryPool,name=PS Survivor Space"
        _attribute                       = "Usage"
        _dict['survivorspace']           = _conn.getAttribute(javax.management.ObjectName(_object),_attribute).get('used')
    
        ## 内存池Meta Space
        _object                          = "java.lang:type=MemoryPool,name=Metaspace"
        _attribute                       = "Usage"
        _dict['metaspace']               = _conn.getAttribute(javax.management.ObjectName(_object),_attribute).get('used')
    
        ## 内存池Compressed Class Space
        _object                          = "java.lang:type=MemoryPool,name=Compressed Class Space"
        _attribute                       = "Usage"
        _dict['compressedclassspace']    = _conn.getAttribute(javax.management.ObjectName(_object),_attribute).get('used')
    
        ## 线程数
        _object                          = "java.lang:type=Threading"
        _attribute                       = "ThreadCount"
        _dict['threadcount']             = _conn.getAttribute(javax.management.ObjectName(_object),_attribute)
    
        ## 读取类数
        _object                          = "java.lang:type=ClassLoading"
        _attribute                       = "TotalLoadedClassCount"
        _dict['classcount']              = _conn.getAttribute(javax.management.ObjectName(_object),_attribute)
    
        ## 打开文件描述符数
        _object                          = "java.lang:type=OperatingSystem"
        _attribute                       = "OpenFileDescriptorCount"
        _dict['openfiledescriptorcount'] = _conn.getAttribute(javax.management.ObjectName(_object),_attribute)
    
        ## 最大允许打开文件描述符数
        _object                          = "java.lang:type=OperatingSystem"
        _attribute                       = "MaxFileDescriptorCount"
        _dict['maxfiledescriptorcount']  = _conn.getAttribute(javax.management.ObjectName(_object),_attribute)
    
        ## 系统逻辑内核数
        _object                          = "java.lang:type=OperatingSystem"
        _attribute                       = "AvailableProcessors"
        _dict['availableprocessors']     = _conn.getAttribute(javax.management.ObjectName(_object),_attribute)
    
        ## 运行时间
        _object                          = "java.lang:type=Runtime"
        _attribute                       = "Uptime"
        _dict['uptime']                  = round(_conn.getAttribute(javax.management.ObjectName(_object),_attribute)/1000,4)
    
        ## 打开子进程数
        _object                          = "java.lang:type=OperatingSystem"
        _attribute                       = "ProcessCpuTime"
        _dict['processcputime']          = round(_conn.getAttribute(javax.management.ObjectName(_object),_attribute)/1000/1000/1000,4)
    
        return _dict

## 程序部分
def main():
    ## 获取jvm虚机位置及连接信息
    jmxLibjvm = osCfg.jmxLibjvm
    jmxConn   = osCfg.jmxConn

    ## 启动jvm虚机
    if not jpype.isJVMStarted():
        jpype.startJVM(jmxLibjvm, convertStrings = False)

    ## 获取项目列表
    projList = [ x for x in jmxConn]

    ## 获取数据列表
    dataList = [ proj_info(
        host = x.get('HostName'), 
        port = x.get('JmxPort'), 
        user = x.get('JmxUser'), 
        passwd = x.get('JmxPass')
        ) for x in jmxConn.values()
    ]    

    ##获取数据字典
    dataDict = dict(zip(projList, dataList))

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
