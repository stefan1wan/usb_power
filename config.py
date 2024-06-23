WEBSITE_NUM = 5 #5 
ACCESS_NUM = 50 #100
ETH_NAME = "enx207bd2e29719" #"enx00e04c680290" #"enx207bd2e29719" #"enx00e04c641532" #"enx00e04c680b2b" #"enxe8e7769bd826"#"enx00e04c641532"#"enxf46b8c7e3040" #"enx803f5df7d521"#"enxf8e43bb03e59"#"enx00e04c680b2b" #"elp"#"enx00e04c680030" # #"enxa0cec88e8a91" #"enx207bd2e29719" #"enxac15a29872ac" "enxa0cec88e8a91" #


import os
import shutil
import time
import psutil
import signal
import json
import numpy as np
from multiprocessing import Process


def read_website_list(filename="website_list.txt"):
    l = open(filename).read().split()
    return l


def parse_website_list(filename="data/website.txt"):
    with open(filename, "r") as file:
        lines = file.readlines()
    websites = [line.strip() for line in lines]
    print(websites)
    assert (len(websites) == WEBSITE_NUM)
    websites_name = [website.split('//')[1] for website in websites]  # ["www.amazon.com", ]

    return websites_name


def make_data_set(input_dir="./preprocessed_data", output_dir="./dataset"):
    data = []
    label = []
    label_dict = {}

    websites_name = parse_website_list()
    for i in range(WEBSITE_NUM):
        label_dict[i] = websites_name[i]

        for j in range(ACCESS_NUM):
            npy_data = input_dir + "/" + websites_name[i] +"_"+ str(j)
            npy_data = np.load(npy_data)
            data.append(npy_data)
            label.append(i)

    data = np.array(data)
    label = np.array(label)
    print("shape of data: ", data.shape)
    print("shape of lable", label.shape)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    np.save(output_dir + "/data.npy", data)
    np.save(output_dir + "/label.npy", label)

    json.dump(label_dict, open(output_dir + "/label_dict.json", "w"))
    print("data set saved to %s" % output_dir)


