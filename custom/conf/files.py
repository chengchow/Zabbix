# coding: utf-8
"""
用于配置监控关键文件和关键目录
"""

## 调用python模块
import sys

## 不允许脚本本地运行
if __name__ == '__main__':
    print(__doc__)
    sys.exit(0)

## 关键文件列表
fileList = [
    '/etc/passwd',
    '/etc/group',
    '/etc/shadow',
    '/etc/sudoers',
    '/etc/resolv.conf',
    '/etc/sysconfig/network',
    '/etc/rc.local',
    '/etc/inittab',
    '/etc/hosts',
    '/etc/hostname',
    '/etc/fstab',
    '/etc/crontab',
    '/etc/motd',
    '/etc/bashrc',
    '/etc/profile',
    '/etc/sysconfig/ip6tables-config',
    '/etc/sysconfig/iptables-config',
    '/etc/ld.so.conf',
    '/etc/sysconfig/firewalld',
    '/etc/sysconfig/crond',
    '/var/spool/mail/root',
]

## 关键目录列表
dirList = [
    '/etc/profile.d',
    '/etc/ld.so.conf.d',
]
