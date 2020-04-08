# -*- coding: utf-8 -*-
"""
参数列表：
    参数1         -->    参数2
    count         -->    number
    percent       -->    use
    times         -->    guest,iowait,system,st,si,idle,hi,user,guest_nict,nice

参数描述:
    number        -->    CPU逻辑核数(个)
    use           -->    CPU当前使用百分比(%)
    guest         -->    guest占用CPU(%)
    iowait        -->    IO等待占用CPU的时间(%)
    system        -->    内核空间占用CPU的时间(%)
    steal         -->    丢失时间占用CPU(%)
    softirq       -->    软件中断占用CPU(%)
    idle          -->    空闲CPU(%)
    irq           -->    硬件中断占用CPU(%)
    user          -->    用户进程占用CPU时间(%)
    guest_nice    -->    guest_nice占用CPU(%)
    nice          -->    改变过优先级的进程占用CPU的时间(%)

标准输出: 浮点数
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
from monitor import cfg,socketTimeout

## 从全局函数文件中引用相应函数
from function import get_initdata

## 设置socket执行超时
socket.setdefaulttimeout(socketTimeout)

## 指定日志格式
cfg.logFormat

## 主程序
def main(**kwargs):
    ## 获取监控项标识
    label = cfg.cpuLabel

    ## 获取缓存文件路径
    cachePath   = os.path.join(cfg.cachePath, label)
    curFileName = cfg.curCache.format(label)
    preFileName = cfg.preCache.format(label)
    curFile     = os.path.join(cachePath, curFileName)
    preFile     = os.path.join(cachePath, preFileName)

    ## 获取结果数据
    try:
        arg1 = kwargs.get('arg1') or sys.argv[1].lower()
        arg2 = kwargs.get('arg2') or sys.argv[2].lower()
    except IndexError:
        logging.error(
            '参数错误, 需要两个参数'
        )
    else:
        if (arg1 =='count' and arg2 =='number') or (arg1 == 'percent' and arg2 == 'use'):
            result = get_initdata(
                arg1     = arg1, 
                arg2     = arg2, 
                jsonFile = curFile
            )
            return result
        elif arg1 =='times':
            curTotal     = get_initdata(
                arg1     = arg1,
                arg2     = 'total',
                jsonFile = curFile
            )
            preTotal = get_initdata(
                arg1     = arg1,
                arg2     = 'total',
                jsonFile = preFile
            )
            curValue = get_initdata(
                arg1     = arg1,
                arg2     = arg2,
                jsonFile = curFile
            )
            preValue = get_initdata(
                arg1     = arg1,
                arg2     = arg2,
                jsonFile = preFile
            )
            if curTotal and preTotal and curValue and preValue:
                diffValue = round(float(curValue) - float(preValue), 2)
                diffTotal = round(float(curTotal) - float(preTotal), 2)
                if diffTotal > 0 and diffValue > 0:
                    result = round(diffValue * 100 / diffTotal , 2)
                    return result
                else:
                    logging.info(
                        '差值为负数或零, 结果归零: diffTotal={}, diffValue = {}'.format(
                        diffTotal, diffValue)
                    )
                    return 0.0
            else:
                logging.error(
                    '数据获取失败: curTotal={}, preTotal={}, curValue={}, preValue={}'.format(
                    curTotal, preTotal, curValue, preValue)
                )
        else:
            logging.error(
                '参数错误, 请查看帮助文档. 当前参数: arg1={} arg2={}'.format(
                arg1, arg2)
            )

## 调试
if __name__ == '__main__':
    if main() is None:
        print(__doc__)
    else:
        print(main())

