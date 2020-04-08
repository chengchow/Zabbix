# -*- coding: utf-8 -*-
"""
参数列表:
    参数1               -->     参数2
    status              -->     active,accepts,handled_requests,server,reading,writing,waiting

参数描述:
    active              -->     表示Nginx正在处理的活动连接数(count)
    accepts             -->     每秒成功创建的握手次数(count/s)
    handled_requests    -->     每秒处理的请求次数(count/s)
    server              -->     每秒处理的链接(count/s)
    reading             -->     读取到客户端的Header信息数(count)
    writing             -->     返回给客户端的Header信息数(count)
    waiting             -->     已经处理完正在等候下一次请求指令的驻留链接(开启keep-alive的情况下, 这个值等于Active-(Reading+Writing)),
                                参考ESTABLISHED状态 
标准输出: 浮点数
作者: zz
版本: v1.0.0
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
from function import get_index, get_sec_index, get_initdata, get_avgdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.nginxLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 获取关键词列表
    keyList = get_index(jsonFile = curFile)

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数'
        )
    else:
        if keyList:
            if arg1 in keyList and arg2 in ('reading', 'writing', 'waiting', 'active'):
                result = get_initdata(
                    arg1     = arg1,
                    arg2     = arg2,
                    jsonFile = curFile
            )
                return result
            elif arg1 in keyList and arg2 in ('accepts', 'handled_requests', 'server'):
                result = get_avgdata(
                    arg1    = arg1,
                    arg2    = arg2,
                    curFile = curFile,
                    preFile = preFile
                )
                return result
            else:
                logging.error(
                    '参数错误, 当前参数: arg1={} arg2={}'.format(
                    arg1, arg2)
                )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
