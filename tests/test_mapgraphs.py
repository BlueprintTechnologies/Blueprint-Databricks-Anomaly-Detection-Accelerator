#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-25 18:53:29 wcobb>
 
"""
#
# standard imports
#
import math
import pandas as pd
import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd
from tqdm import tqdm
import dill

import threat
from threat.core import loader, places
from threat.core import public_address
from threat.core import Cache

def scaled_rgba_v2(this_value:float, dpower:int = 0, min_value:float = 0.0, max_value:float = 1.0):
    if (dpower >= 5):
        color = "red"
        alpha = (this_value - min_value)/(max_value - min_value)
    elif (dpower == 4):
        color = "orange"
        alpha = (this_value - min_value)/(max_value - min_value)
    elif (dpower == 3):
        color = "yellow"
        alpha = (this_value - min_value)/(max_value - min_value)
    elif (dpower == 2):
        color = "green"
        alpha = (this_value - min_value)/(max_value - min_value)
    elif (dpower == 1):
        color = "blue"
        alpha = (this_value - min_value)/(max_value - min_value)
    else:
        color = "indigo"
        alpha = (this_value - min_value)/(max_value - min_value)
    return (color, alpha)

def scaled_rgba(mea, mea_min = 0.05, mea_mid = 2.5, mea_max = 5.0):
    """
    Produces an rgba color based on the range of the data and some
    properties of the distribution...

    """
    R = (1 - (mea_max - mea)/(mea_max - mea_min))
    if (R > 1):
        R = 1
    elif (R < 0):
        R = 0
    G = (1-abs(mea_mid - mea)/mea_mid)
    if (G > 1):
        G = 1
    elif (G < 0):
        G = 0
    B = (mea_max - mea)/(mea_max - mea_min)
    if (B > 1):
        B = 1
    elif (B < 0):
        B = 0
    A = R
    return (R, G, B, A)

def display_protocol_worldmap(population, min_count = 1000, anomaly_scaling = "linear", show_world = False):
    """
    """
    main_title = 24
    pane_title = 18
    pane_text = 16
    uni_latlon = (-76.60532, 2.44091)
    labels = ["duration", "volume", "avpktsz",  "dnuprat",  "pktlenvar", "fwdpktlen", "bwdpktlen"]

    for proto in population.keys():
        locations = population[proto]["metrics"]["path"]
        slatlon = locations["src"]
        dlatlon = locations["dst"]
        npts = len(population[proto]['metrics']['flowrate']['data'])
        if (npts >= min_count):
            ascore = []
            tcolor = []
            for i in range(0, npts):
                asmean = np.mean([population[proto]['metrics'][label]['anomaly_score'][i] for label in labels])
                ascore.append(asmean)
            as_max = np.max(ascore)
            as_mid = as_max / 2
            as_mea = np.mean(ascore)
            as_med = np.median(ascore)
            as_mod = mode(ascore).mode[0]
            as_min = np.min(ascore)
            anomaly_score = ascore.copy()
            print(f"...ascore for {proto} contains {len(np.unique(ascore))} values with:")
            sas = sorted([(anomaly_score[i], i) for i in range(0, len(anomaly_score))], reverse = True)
            #
            # a different approach...
            #
            d1_events = int(len(sas) / 10)
            if (d1_events > 0):
                d1_threshold = sas[d1_events][0]
                print(f"number of d1 events: {d1_events}, d1_threshold = {d1_threshold}")
            else:
                d1_threshold = 0
            d2_events = int(len(sas) / 100)
            if (d2_events > 0):
                d2_threshold = sas[d2_events][0]
                print(f"number of d2 events: {d2_events}, d2_threshold = {d2_threshold}")
            else:
                d2_threshold = 0
            d3_events = int(len(sas) / 1000)
            if (d3_events > 0):
                d3_threshold = sas[d3_events][0]
                print(f"number of d3 events: {d3_events}, d3_threshold = {d3_threshold}")
            else:
                d3_threshold = 0
            d4_events = int(len(sas) / 10000)
            if (d4_events > 0):
                d4_threshold = sas[d4_events][0]
                print(f"number of d4 events: {d4_events}, d4_threshold = {d4_threshold}")
            else:
                d4_threshold = 0
            d5_events = int(len(sas) / 100000)
            if (d5_events > 0):
                d5_threshold = sas[d5_events][0]
                print(f"number of d5 events: {d5_events}, d5_threshold = {d5_threshold}")
            else:
                d5_threshold = 0
            #
            # compute the colors...
            #
            print(f"...preparing colors and labels")
            graph_colors = []
            graph_labels = []
            vector_color = []
            vector_alpha = []
            for i in range(0, npts):
                if (d5_events > 0) and (anomaly_score[i] > d5_threshold):
                    # then it's a d5 event...
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i], dpower = 5, min_value = as_min, max_value = as_max)
                    vector_color.append(color)
                    vector_alpha.append(alpha)
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 100000 event")
                elif (d4_events > 0) and (anomaly_score[i] > d4_threshold):
                    # then it's a d4 event...        
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i], dpower = 4, min_value = as_min, max_value = as_max)
                    vector_color.append(color)
                    vector_alpha.append(alpha)
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 10000 event")
                elif (d3_events > 0) and (anomaly_score[i] > d3_threshold):
                    # then it's a d3 event...        
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i], dpower = 3, min_value = as_min, max_value = as_max)
                    vector_color.append(color)
                    vector_alpha.append(alpha)
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 1000 event")
                elif (d2_events > 0) and (anomaly_score[i] > d2_threshold):
                    # then it's a d2 event...        
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i], dpower = 2, min_value = as_min, max_value = as_max)
                    vector_color.append(color)
                    vector_alpha.append(alpha)
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 100 event")
                elif (d1_events > 0) and (anomaly_score[i] > d1_threshold):
                    # then it's a d1 event...        
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i], dpower = 1, min_value = as_min, max_value = as_max)
                    vector_color.append(color)
                    vector_alpha.append(alpha)
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 10 event")
                else:
                    # then it's just a normal event...
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i], dpower = 0, min_value = as_min, max_value = as_max)
                    vector_color.append(color)
                    vector_alpha.append(alpha)
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append(" common event")

            print(f"...preparing {proto} end points")
            lons = []
            lats = []
            dire = []
            for i in range(0, npts):
                if (slatlon[i] == uni_latlon):
                    lons.append(slatlon[i][0])
                    lats.append(slatlon[i][1])
                    dire.append("outbound")
            for i in range(0, npts):
                if (dlatlon[i] == uni_latlon):
                    lons.append(dlatlon[i][0])
                    lats.append(dlatlon[i][1])
                    dire.append("inbound")
            #
            # okay show time!
            #
            fig, ax = plt.subplots(2, 1, figsize = (32, 36))
            worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
            plt.suptitle(f"Traffic Vectors for {proto}")
            #========================================================================
            #
            # the inbound traffic map...
            #
            #========================================================================
            worldmap.plot(color = "lightgrey", ax = ax[0])
            ax[0].set_xlim((-180.0, 180.0))
            ax[0].set_xlabel("Longitude", fontsize = pane_text)
            ax[0].set_ylim((-90.0, 90.0))
            ax[0].set_ylabel("Latitude", fontsize = pane_text)
            print(f"...inbound {proto} vectors")
            count = 0
            for i in tqdm(range(npts)):
                if (dire[i] == "inbound"):
                    count += 1
                    this_color = vector_color[i]
                    this_alpha = vector_alpha[i]
                    if (anomaly_scaling == "square"):
                        this_alpha = vector_alpha[i]**2
                    elif (anomaly_scaling == "sqrt"):
                        this_alpha = sqrt(vector_alpha[i])
                    elif (anomaly_scaling == "linear"):
                        this_alpha = vector_alpha[i]
                    ax[0].plot([slatlon[i][0], dlatlon[i][0]],
                               [slatlon[i][1], dlatlon[i][1]], 
                               color = this_color,
                               alpha = min((0.10 + this_alpha), 1), # this_alpha
                               lw = 4*(0.25 + 1.75 * this_alpha), # (0.25 + 5 * this_alpha),
                    )
            ax[0].set_title(f"{count} Inbound {proto} Vectors", fontsize = pane_title)
            #
            # create and render the legend...
            #
            legend_handles = []
            for i in range(0, len(graph_colors)):
                this_label = graph_labels[i]
                this_color = graph_colors[i]
                this_patch = mpatches.Patch(color = this_color, label = this_label)
                legend_handles.append(this_patch)
            ax[0].legend(loc = "lower left", handles = legend_handles)
            #========================================================================
            #
            # the outbound traffic map...
            #
            #========================================================================
            worldmap.plot(color = "lightgrey", ax = ax[1])
            ax[1].set_xlim((-180.0, 180.0))
            ax[1].set_xlabel("Longitude", fontsize = pane_text)
            ax[1].set_ylim((-90.0, 90.0))
            ax[1].set_ylabel("Latitude", fontsize = pane_text)
            print(f"...outbound {proto} vectors")
            count = 0
            for i in tqdm(range(npts)):
                if (dire[i] == "outbound"):
                    count += 1
                    this_color = vector_color[i]
                    this_alpha = vector_alpha[i]
                    if (anomaly_scaling == "square"):
                        this_alpha = vector_alpha[i]**2
                    elif (anomaly_scaling == "sqrt"):
                        this_alpha = sqrt(vector_alpha[i])
                    elif (anomaly_scaling == "linear"):
                        this_alpha = vector_alpha[i]
                    ax[1].plot([slatlon[i][0], dlatlon[i][0]],
                               [slatlon[i][1], dlatlon[i][1]], 
                               color = this_color,
                               alpha = min((0.10 + this_alpha), 1), # this_alpha
                               lw = 4*(0.25 + 1.75 * this_alpha), # (0.25 + 5 * this_alpha),
                    )
            ax[1].set_title(f"{count} Outbound {proto} Vectors", fontsize = pane_title)
            #
            # create and render the legend...
            #
            legend_handles = []
            for i in range(0, len(graph_colors)):
                this_label = graph_labels[i]
                this_color = graph_colors[i]
                this_patch = mpatches.Patch(color = this_color, label = this_label)
                legend_handles.append(this_patch)
            ax[1].legend(loc = "lower left", handles = legend_handles)
            #========================================================================
            #
            # save everything...
            #
            #========================================================================
            plt.savefig(os.path.join(places("images"), f"{proto}_traffic.png"))
            if (show_world):
                plt.show()
            else:
                plt.close()
    return None

if (__name__ == "__main__"):
    """
    """
    print("")
    world_graphics = False
    metrics_graphics = False
    population = dill.load(open("/data/blueprint/threat/datasets/updated_population_metrics.dill", "rb"))
    #
    # pass the population data object to the graphics routine...
    #
    display_protocol_worldmap(population, min_count = 1000, anomaly_scaling = "square")
