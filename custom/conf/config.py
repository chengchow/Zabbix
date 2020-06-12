# coding: utf-8
"""
用于配置用户配置选项
"""

## 调用python模块
import sys

## 不允许本地运行
if __name__ == '__main__':
    print(__doc__)
    sys.exit(0)

## 监听端口列表
portList = [
    {"PortName":"sshd 连接", "PortType":"tcp", "HostAddr":"127.0.0.1", "PortNumber":22},
    {"PortName":"zabbix_agentd（客户端）", "PortType":"tcp", "HostAddr":"127.0.0.1", "PortNumber":10050},
    {"PortName":"店管家Api", "PortType":"tcp", "HostAddr":"127.0.0.1", "PortNumber":8187},
    {"PortName":"店管家Console", "PortType":"tcp", "HostAddr":"127.0.0.1", "PortNumber":8212},
    {"PortName":"店管家Callback", "PortType":"tcp", "HostAddr":"127.0.0.1", "PortNumber":8191},
    {"PortName":"店管家Job", "PortType":"tcp", "HostAddr":"127.0.0.1", "PortNumber":8193},
]

## 日志关键词监控信息
logKeys = [
    dict(
        sign         = 'dgjs_callback_threads',
        name         = '店管家CallBack日志Threads错误',
        keyword      = 'java.util.concurrent.ThreadPoolExecutor',
        logdir       = '/home/uenpay/logs/dgjs/callback/{year}{mon}{date}',      ## (year, mon, date)
        doublethorld = 86400
    ),
    dict(
        sign         = 'dgjs_callback_redis',
        name         = '店管家CallBack日志Redis连接错误',
        keyword      = 'Cannot connect Redis Sentinel at',
        logdir       = '/home/uenpay/logs/dgjs/callback/{year}{mon}{date}',      ## (year, mon, date)
        doublethorld = 86400       
    ),
    dict(
        sign         = 'dgjs_callback_db',
        name         = '店管家CallBack日志DB连接错误',
        keyword      = 'java.sql.SQLSyntaxErrorException',
        logdir       = '/home/uenpay/logs/dgjs/callback/{year}{mon}{date}',      ## (year, mon, date)
        doublethorld = 86400       
    ),
]

## 监听进程列表
procList = [
    "chronyd"
]

## Nginx状态URL
ngxUrl = "http://localhost:65455/nginx_status"

## Php状态URL(json输出)
phpUrl = "http://localhost:56535/php_status?json"

## Mysql数据库连接信息, 支持多实例
## 该用户需要show权限，由于密码存放，建议用最小权限用户
mysqlConn = [
    { 'MysqlUser' : 'zbxadmin', 'MysqlPass' : 'Zbx@un1p2y0c0m', 'MysqlHost' : '192.168.254.10', 'MysqlPort' : 3306}
]

## Redis数据库连接信息, 支持多应用
rdsConn = [
    { 'RedisPass' : '', 'RedisHost' : '127.0.0.1', 'RedisPort' : 1111,},
    { 'RedisPass' : '', 'RedisHost' : '127.0.0.1', 'RedisPort' : 2222,}
]

## Jmx(Java)配置信息
jmxLibjvm = "/data/software/java/jre/lib/amd64/server/libjvm.so"
jmxConn = {
    'sss'    : { 'HostName' : '127.0.0.1',      'JmxPort' : 11111, 'JmxUser' : '', 'JmxPass' : ''},
    'ssssss' : { 'HostName' : '192.168.254.10', 'JmxPort' : 22222, 'JmxUser' : '', 'JmxPass' : ''}
}

## URL检测列表
urlInfo = {
    '百度' :     { 'UrlType' : 'https', 'Url' : 'www.baidu.com' },
    '搜狐新闻' : { 'UrlType' : 'http',  'Url' : 'news.sohu.com' }
}

## 域名证书过期检测列表
certInfo = {
    '百度' : { 'CertName' : 'www.baidu.com', 'CertPort' : 443 },
    '搜狐' : { 'CertName' : 'www.sohu.com' , 'CertPort' : 443 }
}

## 域名过期检测列表
dnsInfo = {
    '百度' : 'www.baidu.com',
    '搜狐' : 'www.sohu.com'
}
