#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 vam <edit py/.vimrc to change me>
#
# Distributed under terms of the MIT license.

import os
import shutil
import time
import psutil
import signal
import numpy as np
from multiprocessing import Process



def read_website_list(filename="website_list.txt"):
    l = open(filename).read().split()
    return l
