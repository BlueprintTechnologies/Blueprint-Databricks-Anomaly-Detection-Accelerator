#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:26:34 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-19 11:26:36 wcobb>
 
"""
import os, sys, dill, gzip, time
import pandas as pd
import numpy as np


def num_cpus(output_root="/dev/shm", output_file="num_cpus.txt", verbose=False):
    '''
    Small function for assessing the number of CPUs present 
    on a system. Intended for use in more efficiently using
    resources during 'training'.

    Tested and verified to work on:

       * ubuntu linux 20.04 on 12 core i7-8700K

       * windows 10 wsl2 ubunto 20.04 on 12 core i7-9750H

       * windows 10 native on 12 core i7-9750H powershell
         and command.com

    @TODO:  add support for Darwin (current code defaults to 1 cpu)

    '''
    num_cpus = 1 # there certainly must be at least 1...
    if (sys.platform == "linux"):
        output_path = os.path.join(output_root, output_file)
        if ("microsoft" in os.uname().release):
            if (verbose):
                print("...windows wsl2 linux detected")
        else:
            if (verbose):
                print("...native linux detected")
        # fortunately the same method works for both of these...
        status = os.system(("cat /proc/cpuinfo | egrep 'model name' | wc -l > %s" % output_path))
        if (status == 0):
            with open(output_path, "r") as ofile:
                lines = ofile.readlines()
                if (len(lines) == 1):
                    num_cpus = int(lines[0])
    elif (sys.platform == "darwin"):
        output_path = os.path.join(".", output_file)
        if (verbose):
            print("...native darwin detected.")
        status = os.system(("sysctl -a | egrep 'machdep.cpu.thread_count' > %s" % output_path))
        if (status == 0):
            with open(output_path, "r") as ofile:
                 line = ofile.readline()
            num_cpus = int(line.split(":")[1])
            os.remove(output_path)
    elif ("win" in sys.platform):
        output_path = os.path.join(".", output_file)
        if (verbose):
            print("...native windows detected")
        num_cpus = int(os.environ["NUMBER_OF_PROCESSORS"])
    else:
        if (verbose):
            print("...unknown OS detected. defaulting to 1 cpu")
            num_cpus = 1
    return num_cpus

