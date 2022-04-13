#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-12 10:29:19 wcobb>
 
"""
#
# standard imports
#
import os, gzip
import math
import pandas as pd
import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt
import geopandas as gpd
from tqdm import tqdm
import dill

import threat
from threat.core import loader, places
from threat.core import public_address
from threat.core import Cache

def traffic_proto_ranking(traffic_proto):    
    #
    # define them...
    #
    utp = np.unique(traffic_proto)
    #
    # initialize a dictionary...
    #
    utp_freqs = {}
    for key in utp:
        if (key not in utp_freqs.keys()):
            utp_freqs[key] = 0
    #
    # count them...
    #
    for tp in traffic_proto:
        utp_freqs[tp] += 1
    #
    # rank them...
    #
    ranking = []
    for key in utp_freqs.keys():
        ranking.append((utp_freqs[key], key))
    sranking = sorted(ranking, reverse = True)
    total = np.sum([s for (s,p) in sranking])
    nsranking = [(100*s/total,p) for (s,p) in sranking]
    return nsranking
