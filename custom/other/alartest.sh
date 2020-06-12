#!/bin/bash
#测试触发器脚本


for ((i=1;i<=100;i++));do
    let purge=$i%2
    if [ $purge = 0 ];then
        systemctl start vsftpd
    else
        systemctl stop vsftpd
    fi
    sleep 120
done

exit 0
