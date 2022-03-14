#!/usr/bin/env python
"""
Created on Wednesday, January 19, 2022 at 11:30:39 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-14 09:09:40 wcobb>
 
"""
import os, sys, dill, gzip, time, math
import pandas as pd
import numpy as np

from threat.common import envvar

def filepaths_containing(pattern, search_dir="/tmp", logger=None):
    data_root = envvar(search_dir)
    those_files = os.listdir(data_root)
    these_paths = []
    for this_file in those_files:
        if (pattern in this_file):
            this_path = os.path.join(data_root, this_file)
            these_paths.append(this_path)
    for this_path in these_paths:
        message = f"...found {this_path}"
        if (logger != None):
            logger.info(message)
        else:
            print(message)
    return these_paths

