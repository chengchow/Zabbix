# -*- coding: utf-8 -*-
"""
参数列表:
    参数1             -->    参数2
    netstat           -->    all,closed,listen,syn_recv,syn_sent,established,fin_wait1,fin_wait2,close_wait,closing,time_wait,last_ack

参数描述:
    CLOSED            -->    初始(无连接)状态
    LISTEN            -->    侦听状态, 等待远程机器连接请求
    SYN_RECV          -->    在TCP三次握手期间, 主动连接端收到SYN包后, 进入SYN_RECV状态
    SYN_SENT          -->    在TCP三次握手期间, 主动连接端发送了SYN包后, 进入SYN_SEND状态, 等待对方的ACK包
    ESTABLISHED       -->    完成TCP三次握手后, 主动连接端进入ESTABLISHED状态. 此时, TCP连接已经建立, 可以进行通信
    FIN_WAIT1         -->    在TCP四次挥手时, 主动关闭端发送FIN包后, 进入FIN_WAIT_1状态
    FIN_WAIT2         -->    在TCP四次挥手时, 主动关闭端收到ACK包后, 进入FIN_WAIT_2状态
    CLOSE_WAIT        -->    在TCP四次挥手期间, 被动关闭端收到FIN包后, 进入CLOSE_WAIT状态
    CLOSING           -->    在TCP四次挥手期间, 主动关闭端发送了FIN包后, 没有收到对应的ACK包, 却收到对方的FIN包, 此时, 进入CLOSING状态
    TIME_WAIT         -->    在TCP四次挥手时, 主动关闭端发送了ACK包之后, 进入TIME_WAIT状态, 等待最多MSL时间, 让被动关闭端收到ACK包
    LAST_ACK          -->    在TCP四次挥手时, 被动关闭端发送FIN包后, 进入LAST_ACK状态, 等待对方的ACK包
    ALL               -->    包含所有TCP,UDP,SOCKET等连接

输出类型: 整数
作者: zz
版本: v4.0.0
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
from function import get_initdata, get_index, get_sec_index

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.tcpLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)

    ## 获取关键词列表
    keyList = get_index(jsonFile = curFile)

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数. '
        )
    else:
        secKeyList = get_sec_index(
            arg1     = arg1,
            jsonFile = curFile
        )

        if keyList and secKeyList:
            if arg1 in keyList and arg2 in secKeyList:
                result = int(get_initdata(
                    arg1     = arg1,
                    arg2     = arg2,
                    jsonFile = curFile)
                )
                return result
            else:
                logging.error(
                    '参数不正确，当前参数: arg1={}, arg2={}'.format(
                    arg1, arg2)
                )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
