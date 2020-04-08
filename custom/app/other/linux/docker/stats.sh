#!/bin/bash
## docker.sock权限问题, 开启zabbix sudo权限
## 创建docker用户组，添加zabbix到docker组


DOK_CMD=/usr/bin/docker

DOK_LIST="$DOK_CMD /usr/bin/docker docker"

for i in $DOK_LIST;do
    ${i} --help > /dev/null 2>&1
    if [ `echo $?` = 0 ];then
        DOK_EXEC=$i
        break
    fi
done

sudo $DOK_EXEC stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemPerc}}\t{{.NetIO}}" --no-stream 2>/dev/null | awk 'NR!=1'

#sudo $DOK_EXEC stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemPerc}}" --no-stream | awk 'NR!=1'
