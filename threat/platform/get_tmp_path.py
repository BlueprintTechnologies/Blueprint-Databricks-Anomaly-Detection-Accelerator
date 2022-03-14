#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:25:36 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-01-19 11:25:39 wcobb>
 
"""
import os, sys, dill, gzip, time
import pandas as pd
import numpy as np
import base64

def get_tmp_path(use_shm_if_possible = False):
    """
    Simple little function that returns a platform specific path to 
    a directory for use in writing temporary content.  On linux 
    systems this can be set so as to use the shared memory filesystem
    '/dev/shm' -- which is almost always much faster than a physical
    disk...

    """
    if ((sys.platform == "linux") or (sys.platform == "darwin")):
        if ((sys.platform == "linux") and (use_shm_if_possible == True)):
            return "/dev/shm"
        else:
            return "/tmp"
    else:
        #
        # there are MANY variations of windows and windows-like environments
        # (too many for it to be practical to test for)... most of these are
        # define either "TEMP" or "TMP" as environment variables...
        #
        try:
            return os.environ["TEMP"]
        except Exception as oops:
            #   
            # okay so that didn't work :( one other thing to try...
            #
            try:
                return os.environ["TMP"]
            except Exception as oops2:
                #
                # well if all else fails we can write the temp files to the current working directory
                #
                return "."
    
if (__name__ == "__main__"):
    """
    """
    print("")
    print("get_tmp_path: %s" % get_tmp_path())
