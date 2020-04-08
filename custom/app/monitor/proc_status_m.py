# -*- coding: utf-8 -*-
"""
参数列表:
    参数1              -->    参数2
    status             -->    all,running,sleeping,disk_sleep,stopped,tracing_stop,zombie,dead,wake_kill,waking,parked,idle

参数描述:
    all                -->    当前进程总数(count) 
    running            -->    当前运行或将要运行进程数(R,count)
    sleeping           -->    休眠中, 受阻, 在等待某个条件的形成或接收到信号(S,count)
    disk_sleep         -->    收到信号不唤醒和不可运行, 进程必须等待直到有中断发生(D,count)
    stopped            -->    由于任务的控制或者外部的追踪而被终止(T,count)
    tracing_stop       -->    进程收到SiGSTOP,SIGSTP,SIGTOU信号后停止运行(t,count)
    zombie             -->    当前僵尸进程数(Z,count)
    dead               -->    死掉的进程(X,count)
    wake_kill          -->    (count)
    waking             -->    (WA,count)
    parked             -->    (count)
    idle               -->    (I,count)

输出格式: 整数
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
from function import load_json_file 

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取项目标签
    label = cfg.processLabel

    ## 获取进程状态标签
    procStatsList = osCfg.procStatsList

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)

    ## 获取当前数据
    curDict = load_json_file(curFile)

    ## 获取结果数据
    try:
        statusList = curDict.get('data').get('status')
    except:
        logging.warning(
            '获取进程信息失败: curFile={}'.format(
            curFile)
        )
    else:
        try:
            arg1 = kwargs.get('arg1') or sys.argv[1].lower()
            arg2 = kwargs.get('arg2') or sys.argv[2].lower()
        except IndexError:
            logging.error(
                '参数错误, 需要两个参数'
            )
        else:
            if statusList:
                if arg1 == 'status':
                    if arg2 == 'all':
                        result = statusList
                        return len(result)
                    elif arg2 in procStatsList:
                        arg2 = arg2.replace('_','-')
                        result = [ x for x in statusList if x.get('status') == arg2]
                        return len(result)
                    else:
                        logging.error(
                            '参数2错误, 当前参数2: arg2={}'.format(
                            arg2)
                        )
                else:
                    logging.error(
                        '参数1错误, 当前参数1: arg1={}'.format(
                        arg1)
                    )
            else:
                loggin.warning(
                    '进程列表为空, 请检测缓存文件: curFile={}'.format(
                    curFile)
                )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())
