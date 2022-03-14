#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:26:46 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-19 11:26:47 wcobb>
 
"""
import os, sys, dill, gzip, time
import pandas as pd
import numpy as np

def num_gpus(output_root="/dev/shm",
             dqfile_name="deviceQuery.txt",
             nsfile_name="nvidia-smi.txt",
             lsfile_name="lspci.txt",
             verbose=False):
    '''
    Simple function that attempts to return the number of nvidia
    CUDA gpus present on a system.  It does this in 3 possible
    ways.  It tries to use nvidia-smi (if that can be found) or
    deviceQuery (if that can be found) and finally it tries to
    look at the catalog returned by 'lspci' if we're on linux.

    Testing:
       * works with ubuntu linux on both 1 and 2 gpu systems.

       * works with windows10 wsl2 on 1 gpu system with deviceQuery

       * works with windows10 in windows mode with both
         powershell.exe and command.com

    @TODO: improve robustness

    '''
    #
    # initialize assuming no gpus are present...
    #
    num_gpus = 0
    #
    # we're here if we couldn't find nvidia-smi...
    #
    if (sys.platform == "linux"):
        nsfile_path = os.path.join(output_root, nsfile_name)
        dqfile_path = os.path.join(output_root, dqfile_name)
        lsfile_path = os.path.join(output_root, lsfile_name)
    else:
        # if not linux then don't default to /dev/shm use local directory 
        nsfile_path = os.path.join(".", nsfile_name)
        dqfile_path = os.path.join(".", dqfile_name)
        lsfile_path = os.path.join(".", lsfile_name)
        
    if (os.system(("nvidia-smi 2>/dev/null 1>%s" % nsfile_path)) == 0):
        with open(nsfile_path, "r") as nsfile:
            lines = nsfile.readlines()
            if (len(lines) > 0):
                for line in lines:
                    if (("GeForce" in line) or
                        ("Tesla"   in line) or
                        ("Quadro"  in line)):
                        num_gpus += 1
                if (num_gpus > 0):
                    if (verbose):
                        print("...confirmed presence of %d gpus via nvidia-smi" % num_gpus)
                    return num_gpus
                
    #
    # okay so that didn't work, let's try deviceQuery...
    #
    if (os.system(("deviceQuery 2>/dev/null 1>%s" % dqfile_path)) == 0):
        with open(dqfile_path, "r") as dqfile:
            lines = dqfile.readlines()
            if (len(lines) > 0):
                for line in lines:
                    if ("CUDA Capable device(s)" in line):
                        parts = line.split(" ")
                        num_gpus = int(parts[1])
                        if (verbose):
                            print("...confirmed presence of %d gpus via deviceQuery" % num_gpus)
                        return num_gpus
    #
    # neither nvidia-smi nor deviceQuery worked.
    #
    if ((sys.platform == "linux") and ("microsoft" in os.uname())):
        # appears to WSL platform... check to see what lspci tells
        if (os.system(("lspci > %s" % lsfile_path)) == 0):
            with open(lsfile_path, "r") as info:
                lines = info.readlines()
                for line in lines:
                    if ((("3D" in line)     and ("Microsoft" in line)) or
                        (("NVIDIA" in line) and ("VGA" in line))       or
                        (("3D" in line)     and ("NVIDIA" in line))):
                        #
                        # something is there but don't what for sure, so default to '1'...
                        #
                        if (verbose):
                            num_gpus = 1
                            print("...detected WSL2 system and defaulting to %d gpus" % num_gpus)
                        return num_gpus
    return 0

