#!/bin/bash
ip addr add 10.164.9.107/25 dev $1
ip link set $1 up
ip route add default via 10.164.9.1