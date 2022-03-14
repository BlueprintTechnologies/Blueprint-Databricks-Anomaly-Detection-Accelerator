#!/usr/bin/env python
"""
Created on Monday, March 14, 2022 at 09:36:13 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-14 09:36:28 wcobb>
 
"""
import os, sys, time, math
from tqdm import tqdm
import pandas as pd
import numpy as np
import dill, gzip

from threat.common import Remote, RemoteError

def places(key:str = "?", data_root = "/data", org_name = "blueprint", project_name = "threat") -> str:
    """
    """
    if (sys.platform == "darwin") and (data_root == "/data"):
        #
        # on mac os x the data directory should NOT default to /data
        # instead it should default to ${HOME}/Data...
        #
        project_root = os.path.join(os.environ["HOME"], "Data", org_name, project_name)
    else:
        #
        # anything else we assume the user knows what s/he is doing
        # and we accept their definition...
        #
        project_root = os.path.join(data_root, org_name, project_name)
    #
    # this makes sure that the project root data directory exists...
    #
    remote_created = False
    if (not os.path.exists(project_root)):
        remote = Remote()
        remote_created = True
        remote.mkdir(project_root)
    #
    # declare the core project locations...
    #
    locations = {"datasets": os.path.join(project_root, "datasets"),
                 "images":   os.path.join(project_root, "images"),
                 "masks":    os.path.join(project_root, "masks"),
                 "models":   os.path.join(project_root, "models"),
                 "extras":   os.path.join(project_root, "extras"),
                 "other":    os.path.join(project_root, "other"),
                 "logfiles": os.path.join(project_root, "logfiles"),
    }
    if (key == "?") or (key == "help"):
        return f"{list(locations.keys())}"
    else:    
        #
        # this handles any missing directories...
        #
        for this_key in locations.keys():
            if (not os.path.exists(locations[this_key])):
                if (not remote_created):
                    remote = Remote()
                    remote_create = True
                remote.mkdir(locations[this_key])
        #
        # this returns the value for the requested key...
        #
        if (key in list(locations.keys())):
            return locations[key]
        else:
            raise RuntimeError(f"unknown location key '{key}'")
    

