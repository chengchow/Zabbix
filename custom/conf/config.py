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
    { "PortName" : "sshd 连接"            , "HostAddr" : "192.168.254.10", "PortType" : "tcp", "PortNumber" : 22    },
    { "PortName" : "zabbix_agentd(客户端)", "HostAddr" : "127.0.0.1",      "PortType" : "tcp", "PortNumber" : 10050 },
    { "PortName" : "zabbix_server"        , "HostAddr" : "127.0.0.1",      "PortType" : "tcp", "PortNumber" : 10051 },
    { "PortName" : "nginx"                , "HostAddr" : "127.0.0.1",      "PortType" : "tcp", "PortNumber" : 80    },
    { "PortName" : "nginx_status"         , "HostAddr" : "127.0.0.1",      "PortType" : "tcp", "PortNumber" : 65455 },
    { "PortName" : "mysqld"               , "HostAddr" : "127.0.0.1",      "PortType" : "tcp", "PortNumber" : 3306  }
]

## 监听进程列表
procList = [
    "sshd",
    "zabbix_agentd",
    "zabbix_server",
    "nginx",
    "mysqld"
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
    'rms'    : { 'HostName' : '127.0.0.1',      'JmxPort' : 19013, 'JmxUser' : '', 'JmxPass' : ''},
    'uenrms' : { 'HostName' : '192.168.254.10', 'JmxPort' : 18280, 'JmxUser' : '', 'JmxPass' : ''}
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
