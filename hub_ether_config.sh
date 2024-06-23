#!/bin/bash

# 检查参数个数
if [ "$#" -ne 1 ]; then
    echo "使用方法: $0 [网卡名称]"
    exit 1
fi
echo "Ethernet Device: $1";

# sudo su
ip netns add ns-s2
ip link set $1 netns ns-s2
ip netns exec ns-s2 bash ./hub_ns_config.sh $1

# ip netns exec ns-s2 ping 10.164.9.126

ip netns exec ns-s2 iptables -t nat -A OUTPUT -p udp --dport 53 -j DNAT --to-destination 128.210.11.5
ip netns exec ns-s2 iptables -t nat -A OUTPUT -p tcp --dport 53 -j DNAT --to-destination 128.210.11.5