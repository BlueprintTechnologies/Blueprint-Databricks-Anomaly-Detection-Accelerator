#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-12 10:32:56 wcobb>
 
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
from threat.core import traffic_proto_ranking

def display_world(slatlon, dlatlon, traffic_color, dur, bps, show_world = False):
    """
    """
    fig, ax = plt.subplots(2, 1, figsize = (24, 24))
    worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    worldmap.plot(color = "lightgrey", ax = ax[0])
    #
    # the inbound traffic map...
    #
    main_title = 24
    pane_title = 18
    pane_text = 16
    plt.suptitle("Network Traffic", fontsize = main_title)
    ax[0].set_title("Inbound", fontsize = pane_title)
    ax[0].set_xlim((-180.0, 180.0))
    ax[0].set_xlabel("Longitude", fontsize = pane_text)
    ax[0].set_ylim((-90.0, 90.0))
    ax[0].set_ylabel("Latitude", fontsize = pane_text)
    ax[0].scatter(lons, lats, marker = ",", s = 1, alpha = 0.10, color = "black")
    #
    # the traffic direction vectors...
    #
    print("...inbound traffic vectors")
    for i in tqdm(range(len(bps))):
        if (traffic_color[i] == "green"):
            ax[0].plot([slatlon[i][0], dlatlon[i][0]], [slatlon[i][1], dlatlon[i][1]],
                       color = traffic_color[i], lw = dur[i], alpha = bps[i])
    #
    # the outbound traffic map...
    #
    worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    worldmap.plot(color = "lightgrey", ax = ax[1])
    #
    # the various endpoints...
    #
    ax[1].set_title("Outbound", size = pane_title)
    ax[1].set_xlim((-180.0, 180.0))
    ax[1].set_xlabel("Longitude", size = pane_text)
    ax[1].set_ylim((-90.0, 90.0))
    ax[1].set_ylabel("Latitude", size = pane_text)
    ax[1].scatter(lons, lats, marker = ",", s = 1, alpha = 0.10, color = "black")
    #
    # the traffic direction vectors...
    #
    print("...outbound traffic vectors")
    for i in tqdm(range(len(bps))):
        if (traffic_color[i] == "red"):
            ax[1].plot([slatlon[i][0], dlatlon[i][0]], [slatlon[i][1], dlatlon[i][1]],
                       color = traffic_color[i], lw = dur[i], alpha = bps[i])
    plt.savefig(os.path.join(places("images"), "all_traffic.png"))
    if (show_world):
        plt.show()
    else:
        plt.close()
    return None
