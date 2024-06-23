#!/bin/bash
# sudo ./hub_ether_config.sh enxac15a29872ac
#ETH_NAME=enxac15a29872ac # TPLINK
# ETH_NAME=enx207bd2e29719 # UGREEN
# ETH_NAME=enxa0cec88e8a91 # ANKER
#ETH_NAME=enx00e04c641532 # UNI
#ETH_NAME=enx00e04c680030 # Fophmo
# ETH_NAME=enx00e04c680b2b # 10 Gbps Getatek
# ETH_NAME=enxf8e43bb03e59 # 10 Gbps RSHTECH
# ETH_NAME=enx803f5df7d521 # WAVLINK
# ETH_NAME=enxf46b8c7e3040 # dell monitor
ETH_NAME=enx00e04c680290 # 10 Gbps Inateck
sudo -E ./hub_ether_config.sh $ETH_NAME
sudo -E python3 power_collect.py --num 100 --eth $ETH_NAME
