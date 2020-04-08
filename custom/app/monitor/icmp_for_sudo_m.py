# -*- coding: utf-8 -*-
"""
参数列表:
    参数1              -->     参数2
    icmp               -->     检测地址(例如: www.baidu.com, 127.0.0.1)

参数描述:
    1                  -->     连接正常
    0                  -->     连接不正常

输出格式: 整数或者字符
作者: zz
版本: v1.0.0
备注: 需要root权限, 有条件情况下推荐该脚本检测
"""
## 导入python模块
import os,sys,socket
import struct
import array

## 导入全局变量和函数
NowPath=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(NowPath,'../../'))

from config import Cfg,PerCmdMaxTime

## 设置脚本命令执行时间限制
socket.setdefaulttimeout(PerCmdMaxTime)

## 规范参数和设置帮助文档
if len(sys.argv)==3:
    Type=sys.argv[1].lower()
    Value=sys.argv[2].lower()
elif len(sys.argv)==1 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print("用法: python" + __file__ +" 参数1 参数2 ")
    print(__doc__)
    sys.exit(0)
else:
    print('参数错误! 查看帮助文档: python '+__file__+' --help')
    sys.exit(0)

if Type != "icmp":
    sys.exit(__doc__)


class Pinger(object):
    def __init__(self,timeout=1):
        self.timeout = timeout
        self.__id = os.getpid()
        self.__data = struct.pack('h',1)#h代表2个字节与头部8个字节组成偶数可进行最短校验

    @property
    def __icmpSocket(self):#返回一个可以利用的icmp原对象,当做属性使用
        icmp = socket.getprotobyname("icmp")#指定服务
        sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)#socket.SOCK_RAW原生包
        return sock

    def __doCksum(self,packet):#校验和运算
        words = array.array('h',packet)#将包分割成2个字节为一组的网络序列
        sum = 0
        for word in words:
            sum += (word & 0xffff)#每2个字节相加
        sum = (sum >> 16) + (sum & 0xffff)#因为sum有可能溢出16位所以将最高位和低位sum相加重复二遍
        sum += (sum >> 16) # 为什么这里的sum不需要再 & 0xffff 因为这里的sum已经是16位的不会溢出,可以手动测试超过65535的十进制数字就溢出了
        return (~sum) & 0xffff #最后取反返回完成校验

    @property
    def __icmpPacket(self):#icmp包的构造
        header = struct.pack('bbHHh',8,0,0,self.__id,0)
        packet = header + self.__data
        cksum = self.__doCksum(packet)
        header = struct.pack('bbHHh',8,0,cksum,self.__id,0)#将校验带入原有包,这里才组成头部,数据部分只是用来做校验所以返回的时候需要返回头部和数据相加
        return header + self.__data 


    def sendPing(self,target_host):
        
        try:
            socket.gethostbyname(target_host)

            sock = self.__icmpSocket
            sock.settimeout(self.timeout)

            packet = self.__icmpPacket

            sock.sendto(packet,(target_host,1))#发送icmp包

            ac_ip = sock.recvfrom(1024)[1][0]
#            print('[+] %s active'%(ac_ip))

            return 1
        except Exception as e:
            sock.close()
            return 0

s = Pinger()

result=s.sendPing(sys.argv[2])

print(result)
