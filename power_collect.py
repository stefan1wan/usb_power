#! /usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *

import time
from tqdm import tqdm
import argparse


PROBE_DIR = "./"


def run_proc(cmd_name, CPU):
    p = psutil.Process()
    p.cpu_affinity([CPU])
    print('EXECUTING: %s (%s)...' % (cmd_name, os.getpid()))
    # TODO: fix the root GPL issue without timeout
    # os.system("timeout 20s " + cmd_name + " >> ./auto_collect_logs.txt 2>&1")
    os.system("timeout 20s " + cmd_name)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='collect data')
    parser.add_argument('--num', type=int, default=150, help='number of samples')
    parser.add_argument('--eth', type=str, default="enxac15a29872ac", help='ethernet probe')
    args = parser.parse_args()
    website_list = read_website_list("website.txt")
    NUM_website = len(website_list)

    NUM_access = args.num
    LOGS_DIR = PROBE_DIR + "logs_%dC_%dA-%s/"%(NUM_website, NUM_access, args.eth)
    if not os.path.exists(LOGS_DIR):
        os.mkdir(LOGS_DIR)

    print("ETH: ", args.eth)
    print("NUM_access: ", NUM_access)
    print("NUM_website: ", NUM_website)
    print("PROBE_DIR: ", PROBE_DIR)
    print("LOGS_DIR: ", LOGS_DIR)
    print("website_list: ", website_list)


    for j in tqdm(range(0, NUM_access)):
        for i in range(NUM_website):
            site = website_list[i]
            site_name = site.split('/')[2]
            # print("Accessing: ", site_name)
            time.sleep(1)


            access_website_cmd = "ip netns exec ns-s2  google-chrome --headless=new --new-window --incognito --disable-application-cache --disable-gpu --no-sandbox --print-to-pdf=%s.pdf %s" % (site_name, site)
            probe_cmd = "python3 ./fnb48p_logger.py" #PROBE_DIR+'io_uringProbe'

            cp_cmd = "cp "+ PROBE_DIR + "/records.npy " + LOGS_DIR  + site_name + "_" + str(j)
            #chwon_cmd = "; chmod 777 " + LOGS_DIR + site_name + "_" + str(j)
            

            # delete lock if any
            os.system("rm -f /home/vam/.config/google-chrome/SingletonLock")
            os.system("./hub_ether_config.sh  %s"%(args.eth))
            
            CPU_probe = 1 # isolated
            CPU_access = 3 # normal
            time_line = Process(target=run_proc, args=(probe_cmd, CPU_probe))
            ac_net = Process(target=run_proc, args=(access_website_cmd, CPU_access))

            time_line.start()
            # print("Waiting for 1s before access....................")
            time.sleep(1)
            ac_net.start()
            time_line.join()
            ac_net.join()

            os.system(cp_cmd )
    os.system("chmod "+" -R " +" 777 "+ LOGS_DIR)