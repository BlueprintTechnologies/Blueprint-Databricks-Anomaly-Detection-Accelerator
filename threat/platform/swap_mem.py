#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:27:11 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-19 11:27:13 wcobb>
 
"""
import os, sys, dill, gzip, time
import pandas as pd
import numpy as np

def swap_mem(output_root="/dev/shm", output_file="swap_mem.txt", verbose=False):
    '''
    Swap Memory of this System in Gigabytes

    Testing:
        * known to work properly on native linux ubuntu

    '''
    swap_mem = 4
    if (sys.platform == "linux"):
        output_path = os.path.join(output_root, output_file)
        if ("microsoft" in os.uname().release):
            if (verbose):
                print("...windows wsl2 linux detected")
        else:
            if (verbose):
                print("...native linux detected")
        #
        # fortunately the same method works for both of these...
        #
        status = os.system(("free -m > %s" % output_path))
        if (status == 0):
            with open(output_path, "r") as ofile:
                lines = ofile.readlines()
                for line in lines:
                    if ("Swap:" in line):
                        line = line.replace("    "," ").replace("   "," ").replace("  "," ").replace("  "," ").replace("  "," ")
                        parts = line.split(" ")
                        swap_mem = 4*int((int(parts[1]) + 2048)/4096)
                        
    elif (sys.platform == "darwin"):
        output_path = os.path.join(".", output_file)
        if (verbose):
            print("...native darwin detected. defaulting to 4096 MB")
    elif ("win" in sys.platform):
        output_path = os.path.join(".", output_file)
        if (verbose):
            print("...native windows detected. defaulting to 4096 MB")
    else:
        if (verbose):
            print("...unknown OS detected. defaulting to 4096 MB")
            
    return swap_mem

