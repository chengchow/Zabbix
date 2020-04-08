# coding: utf-8
"""
备注 : 用于监控通用变量及系统变量定义,windows部分未完成.
作者 : zz
版本 : v4.0.0

"""

## 调用python模块
import os, sys, re
import psutil
import logging

## 指定python执行路径
pyExec = "/usr/bin/python"

## 设置缓存执行模式(True|False)
cacheType = True

## 缓存执行时间间隔(仅在CacheAuto = True时有效. 取值: 整数，单位: 秒)
cacheTime = 60

## 自动发现运行时间间隔，单位(秒)
# autoFindTime = 60

## 命令执行socket超时时间(单位: 秒)
socketTimeout = 1.0

## 当前目录和根目录
nowPath  = os.path.dirname(os.path.abspath(__file__))
homePath = nowPath

## 全局变量定义
class general():
    ## 全局子目录位置
    appPath    = os.path.join(homePath,'app')
    cachePath  = os.path.join(homePath,'cache')
    tmpPath    = os.path.join(homePath,'tmp')
    logPath    = os.path.join(homePath,'logs')
    confPath   = os.path.join(homePath,'conf')

    ## 监控脚本路径
    monitorAppPath = os.path.join(appPath,'monitor')
    cacheAppPath   = os.path.join(appPath,'cache')
    findAppPath    = os.path.join(appPath,'find')
    otherAppPath   = os.path.join(appPath,'other')

    ## 日志文件
    logFile = os.path.join(logPath, 'monitor.log')
    
    ## 配置全局日志格式
    logFormat = logging.basicConfig(
        ## 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL, 默认是WARNING
        level    = logging.DEBUG,
        ## 日志格式: 时间, 代码所在文件名, 代码行号, 日志级别名字, 日志信息
        format   = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
        ## 日志打印时间
        datefmt  = "%Y/%m/%d %H:%M:%S %p",
        ## 日志目录
        filename = logFile,
        ## 打印日志方式 w 或 a
        filemode = 'a'
    )

    ## 当前缓存文件前缀
    curCache = 'cur_{}.json'

    ##之前缓存文件前缀
    preCache = 'pre_{}.json'

    ## 监控项标签 
    bootTimeLabel        = 'boot_time'
    certLabel            = 'cert'
    cpuLabel             = 'cpu'
    diskioLabel          = 'diskio'
    dockerLabel          = 'docker'
    domainNameLabel      = 'domain_name'
    fileLabel            = 'file'
    icmpLabel            = 'icmp'
    jmxLabel             = 'jmx'
    loadavgLabel         = 'loadavg'
    memoryLabel          = 'memory'
    mysqlLabel           = 'mysql'
    nginxLabel           = 'nginx'
    partitionLabel       = 'partition'
    phpLabel             = 'php'
    portExistLabel       = 'port_exist'
    processLabel         = 'process'
    procAnalyzeLabel     = 'proc_analyze'
    procExistLabel       = 'proc_exist'
    procStatusLabel      = 'proc_status'
    redisLabel           = 'redis'
    sensorLabel          = 'sensor'
    tcpLabel             = 'tcp'
    trafficLabel         = 'traffice'
    urlLabel             = 'url'
    userLabel            = 'user'

    cacheProjList = ['cpu', 'diskio', 'docker', 'file', 'jmx', 'memory', 'mysql', 'nginx', 'partition', 'php','redis', 'sensor', 'tcp', 'traffic', 'process', 'proc_status', 'proc_analyze', 'proc_exist']

## Linux系统变量
class linux():
    ## 添加conf目录到全局环境路径中
    sys.path.append(general.confPath)    
    import config, files

    ## 调用全局类变量
    selfCfg   = general()
    shellPath = os.path.join(selfCfg.otherAppPath,'linux')

    ## 端口, 进程预警失效文件
    thorldSheildFile = '/tmp/publish.sign'

    ## 关键文件列表
    fileList = files.fileList

    ## 关键目录列表
    dirList  = files.dirList

    ## 关键端口列表
    portList = config.portList

    ## 关键进程列表
    procList = config.procList

    ## TCP连接状态列表
    tcpStatsList = [
        'all',
        'closed',
        'listen',
        'syn_recv',
        'syn_sent',
        'established',
        'fin_wait1',
        'fin_wait2',
        'close_wait',
        'closing',
        'time_wait',
        'last_ack'
    ]

    ## 进程状态列表
    procStatsList = [
        'running',
        'sleeping',
        'disk_sleep',
        'stopped',
        'tracing_stop',
        'zombie','dead',
        'wake_kill',
        'waking',
        'parked',
        'idle'
    ]

    ## 进程信息关键词列表
#    procKeyList = ['name', 'status', 'pid']
    procKeyList = [
        'pid',
        'username',
        'ppid',
        'cpu_percent',
        'memory_info',
        'memory_percent',
        'status','uids',
        'io_counters',
        'create_time',
        'name'
    ]

    ## Nginx信息获取地址及Nginx状态列表
    ngxUrl     = config.ngxUrl
    ngxKeyList = [
        'active',
        'server',
        'accepts',
        'handled_requests',
        'reading',
        'writing',
        'waiting'
    ]

    ## Php信息获取地址 
    phpUrl      = config.phpUrl

    ## Mysql连接信息
    mysqlConn   = config.mysqlConn

    ## Redis连接信息
    rdsConn     = config.rdsConn

    ## Jmx(Jav)连接信息
    jmxLibjvm   = config.jmxLibjvm
    jmxConn     = config.jmxConn

    ## URL检测列表
    urlInfo     = config.urlInfo
    
    ## 证书URL检测列表
    certInfo    = config.certInfo

    ## 域名检测列表
    dnsInfo     = config.dnsInfo

    ## 分区名称列表
    partList    = [ x.mountpoint for x in psutil.disk_partitions() ]

    ## 磁盘名称列表
    diskList    = [ x for x in psutil.disk_io_counters(perdisk = True) if not re.findall('(dm|sr|fd|\d+)', x) ] 

    ## 网络设配器名称列表
    netcardList = [ x for x in psutil.net_io_counters(pernic = True) ]

    ## Docker监控脚本路径
    dockerShell = os.path.join( shellPath, 'docker/stats.sh' )

## windows变量定义
class windows():
    selfCfg = general()

    ## 进程状态列表
    procStatusList = [
        "running",
        'sleeping',
        'disk-sleep',
        'stopped',
        'tracing-stop',
        'zombie','dead',
        'wake-kill',
        'waking'
    ]

cfg = general()

## 识别操作系统类型(linux|windows)
if psutil.LINUX == True:
    osCfg = linux()
elif psutil.WINDOWS == True:
    osCfg = windows()

## 本地调试
if __name__ == '__main__':
    print(__doc__)
