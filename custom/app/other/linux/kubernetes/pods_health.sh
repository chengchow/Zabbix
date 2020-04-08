#!/bin/bash

NOW_PATH=$(cd `dirname $0`;pwd)

. $NOW_PATH/../env.sh

KUBE_CMD=$(grep -Piv '(^#|^$)' $GLOBAL_CFG | grep -Pio "(?<=KubectlCmd=')[^']+")

if [ ! -x $KUBE_CMD ];then
    KUBE_CMD=kubectl
fi

OUTPUT_INFO=$($KUBE_CMD get pods --all-namespaces -o json)

echo $OUTPUT_INFO
