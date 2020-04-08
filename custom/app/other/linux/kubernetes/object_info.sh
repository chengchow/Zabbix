#!/bin/bash

NOW_PATH=$(cd `dirname $0`;pwd)

. $NOW_PATH/../env.sh

KUBE_CMD=$(grep -Piv '(^#|^$)' $GLOBAL_CFG | grep -Pio "(?<=KubectlCmd=')[^']+")

if [ ! -x $KUBE_CMD ];then
    KUBE_CMD=kubectl
fi

case $1 in
    node)
        OUTPUT_INFO=$($KUBE_CMD get nodes | awk 'NR!=1{print $1}')
        ;;
    pod)
        OUTPUT_INFO=$($KUBE_CMD get pods --all-namespaces | awk 'NR!=1{print $2}')
        ;;
    *)
        echo -e "Usage: `basename $0` (node|pod)"
        ;;
esac

echo $OUTPUT_INFO
