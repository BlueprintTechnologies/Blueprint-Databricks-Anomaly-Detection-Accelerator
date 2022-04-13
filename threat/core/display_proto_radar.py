#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-12 10:37:45 wcobb>
 
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
from math import log10, pi, sqrt
import seaborn as sns
import bokeh

import threat
from threat.core import loader, places
from threat.core import public_address
from threat.core import Cache
from threat.common import scaled_rgba_v2

def display_proto_radar(population:{},
                        min_count:int = 1000,
                        pseudo_sigmae:int = 5,
                        anomaly_strategy:str = "mean", # "mean" or "max"...
                        alpha_scaling:str = "linear",  # "sqrt", "linear", or "square"...
                        dark_background:bool = False,
                        black_facecolor:bool = False,
                        display_graphics:bool = False):
    """
    We do NOT have gaussian statistics here (things are definitely 
    NOT in a 'normal' distribution. So we're working with a sort of
    pseudo_sigma in place of standard deviation.

    We define the pseudo_sigma as follows:



    @TODO: please improve this documentation

    """
    ##
    ## the labels for the radial coordinates...
    ##
    theta_labels = [#"flowrate",
                    "duration", "volume",
                    "avpktsz",  "dnuprat",  "pktlenvar",
                    "fwdpktlen", "bwdpktlen",
                   # "actmean",
                   ]
    ##
    ## prepare the angular coordinates to be plotted...
    ##
    theta = [(2*pi*i/len(theta_labels)) for i in range(0, len(theta_labels))]
    for proto in population.keys():
        if (population[proto]["metrics"]["flowrate"]["count"] >= min_count):
            print(f"...preparing radar plot for {proto}")
            ##
            ## prepare the radial coordinates to be plotted...
            ##
            for theta_label in theta_labels:
                num_values  = population[proto]["metrics"][theta_label]["count"]
                data        = population[proto]["metrics"][theta_label]["data"]
                data_min    = np.min(data)
                data_max    = np.max(data)
                data_mean   = population[proto]["metrics"][theta_label]["mean"]
                data_median = population[proto]["metrics"][theta_label]["median"]
                data_std    = population[proto]["metrics"][theta_label]["std"]
                data_mode   = population[proto]["metrics"][theta_label]["mode"]
                ##
                ## our definition of anomaly (as defined in terms of pseudo_sigma)
                ## may indicate that nothing IS an anomaly... that's fine...
                ##
                data_range = data_max - data_min
                data_pos   = abs(data_max - data_mode)
                data_neg   = abs(data_mode - data_min)
                if (data_pos > 0) and (data_neg > 0):
                    pseudo_sigma = np.mean([data_pos, data_neg]) / (pseudo_sigmae + 1)
                elif (data_pos > 0):
                    pseudo_sigma = data_pos / (pseudo_sigmae + 1)
                elif (data_neg > 0):
                    pseudo_sigma = data_neg / (pseudo_sigmae + 1)
                #
                # assigns an anomaly score on (0, pseudo_sigmae) to each of the various 'theta_labels' axes...
                #
                population[proto]["metrics"][theta_label]["anomaly_score"] = [abs(
                    d-data_mode)/pseudo_sigma for d in data]
            ##
            ## define the mean anomaly score for setting the color of the curves...
            ##
            anomaly_score = []
            for i in range(0, len(population[proto]["metrics"][theta_labels[0]]["data"])):
                if (anomaly_strategy == "mean"):
                    anomaly_score.append(np.mean(
                        [population[proto]["metrics"][theta_label]["anomaly_score"][i] for theta_label in theta_labels]))
                elif (anomaly_strategy == "max"):
                    anomaly_score.append(np.max(
                        [population[proto]["metrics"][theta_label]["anomaly_score"][i] for theta_label in theta_labels]))
            ##
            ## prepare the radial coordinates to be plotted...
            ##
            radius = []
            for i in range(0, len(population[proto]["metrics"][theta_labels[0]]["data"])):
                radius.append(
                    [population[proto]["metrics"][theta_label]["anomaly_score"][i] for theta_label in theta_labels])
            ##
            ## create the figure...
            ##
            fig = plt.figure(figsize=(20,16))
            ax = fig.add_subplot(111, polar=True)
            ax.grid(True, lw=0.25)
            ##
            ## conditional appearance tweaks...
            ##
            if (dark_background):
                plt.style.use('dark_background')
            if (black_facecolor):
                plt.rcParams['axes.facecolor'] = 'black'
            plt.title(f"Radar Plots of Feature Data for {len(anomaly_score)} {proto} Transactions",
                      fontsize=24, pad=24)
            plt.xlim((0, 2*pi))
            ##
            ## setting the radial scale...
            ##
            max_radius = math.ceil(np.max(radius))
            ax.set_rmax(max_radius) # new version using max_radius...
            ##
            ## choose the radial tick-marks to be drawn
            ##
            ax.set_rticks([r*0.5 for r in range(0, 2 * max_radius)]) # new version using max_radius...
            plt.xticks(theta, theta_labels, fontsize = 16)
            ans_min = np.min(anomaly_score)
            ans_max = np.max(anomaly_score)
            ans_mid = ans_max/2
            ans_med = np.median(anomaly_score)
            ans_mod = mode(anomaly_score).mode[0]
            ans_mea = np.mean(anomaly_score)
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
            graph_colors = []
            graph_labels = []
            legend_stuff = []
            for i in range(0, len(radius)):
                ##
                ## define the color for this particular curve...
                ##
                if (d5_events > 0) and (anomaly_score[i] > d5_threshold):
                    # then it's a d5 event...
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i],
                                                    dpower = 5,
                                                    min_value = ans_min,
                                                    max_value = ans_max,
                    )
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 100000 event")
                    
                elif (d4_events > 0) and (anomaly_score[i] > d4_threshold):
                    # then it's a d4 event...        
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i],
                                                    dpower = 4,
                                                    min_value = ans_min,
                                                    max_value = ans_max,
                    )
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 10000 event")
                        
                elif (d3_events > 0) and (anomaly_score[i] > d3_threshold):
                    # then it's a d3 event...        
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i],
                                                    dpower = 3,
                                                    min_value = ans_min,
                                                    max_value = ans_max,
                    )
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 1000 event")
                    
                elif (d2_events > 0) and (anomaly_score[i] > d2_threshold):
                    # then it's a d2 event...        
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i],
                                                    dpower = 2,
                                                    min_value = ans_min,
                                                    max_value = ans_max,
                    )
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 100 event")
                    
                elif (d1_events > 0) and (anomaly_score[i] > d1_threshold):
                    # then it's a d1 event...        
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i],
                                                    dpower = 1,
                                                    min_value = ans_min,
                                                    max_value = ans_max,
                    )
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append("1 in 10 event")
                    
                else:
                    # then it's just a normal event...
                    (color, alpha) = scaled_rgba_v2(anomaly_score[i],
                                                    dpower = 0,
                                                    min_value = ans_min,
                                                    max_value = ans_max,
                    )
                    if (color not in graph_colors):
                        graph_colors.append(color)
                        graph_labels.append(" common event")

                this_theta = theta.copy()
                this_theta.append(theta[0])
                this_radius = radius[i].copy()
                this_radius.append(radius[i][0])
                if (alpha_scaling == "sqrt"):
                    plt.plot(this_theta,
                             this_radius,
                             lw=2*(0.20 + sqrt(alpha)),
                             ls="-",
                             color = color,
                             alpha = sqrt(alpha),
                    )
                elif (alpha_scaling == "square"):
                    plt.plot(this_theta,
                             this_radius,
                             lw=2*(0.20 + alpha**2),
                             ls="-",
                             color = color,
                             alpha = alpha**2,
                    )
                elif (alpha_scaling == "linear"):
                    plt.plot(this_theta,
                             this_radius,
                             lw=2*(0.20 + alpha),
                             ls="-",
                             color = color,
                             alpha = alpha,
                    )
                else:
                    raise RuntimeError(f"Don't grok alpha_scaling == {alpha_scaling}")
            #
            # create and render the legend...
            #
            legend_handles = []
            for i in range(0, len(graph_colors)):
                this_label = graph_labels[i]
                this_color = graph_colors[i]
                this_patch = mpatches.Patch(color = this_color, label = this_label)
                legend_handles.append(this_patch)
            ax.legend(loc = "lower left",
                      handles = legend_handles,
                      fontsize=14,
            )
            #
            # save things...
            #
            plt.savefig(os.path.join(places("images"), f"{proto}_radar.png"))
            if (display_graphics):
                plt.show()
            else:
                plt.close()
                
    updated_population_path = os.path.join(places("datasets"), "updated_population_metrics.dill.gz")
    dill.dump(population, gzip.open(updated_population_path, "wb"))
    return None
