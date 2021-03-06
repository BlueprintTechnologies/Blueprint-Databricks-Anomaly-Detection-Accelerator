#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-12 10:38:15 wcobb>
 
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
from threat.common import display_proto_radar

if (__name__ == "__main__"):
    """

    """
    print("\nrunning test_am...")
    anomaly_strategy = "mean"
    display_graphics = False
    alpha_scaling = "square"
    show_histograms = False
    pseudo_sigmae = 5
    min_count = 100 # could be 30, 100, 300, 1000, 3000, etc
    main_title = 24
    pane_title = 18
    pane_text = 16
    num_bins = 10

    ##
    ## load the already-existing data...
    ##
    population_name = "population_metrics.dill.gz"
    population_path = os.path.join(places("datasets"), population_name)
    if (not os.path.exists(population_path)):
        raise RuntimeError(f"Yikes!  Can't find {population_path}... have you run test_cachemap.py yet?")
    
    population = dill.load(gzip.open(population_path, "rb"))
    
    colors = [
        "indigo", "darkblue", "blue",
        "darkcyan", "green", "lightgreen",
        "yellow", "orange", "red",
    ]

    print("...histograms")
    for proto in population.keys():
        #
        # we're going to make 1 figure for each quantity for which we have at least 'min_count' observations
        #
        if (population[proto]["metrics"]["flowrate"]["count"] >= min_count):
            #
            # create the overall image and add the title...
            #
            fig, ax = plt.subplots(3, 3, figsize=(30, 30))
            plt.suptitle(f"Key Histograms for {proto}", fontsize = main_title)
            #
            # 1st col, 1st row...
            #
            ax[0][0].set_title("Flow Rate (bytes/sec)", fontsize = pane_title)
            ax[0][0].set_xlabel("Bin", fontsize = pane_text)
            ax[0][0].set_ylabel("log10(Counts)", fontsize = pane_text)
            ax[0][0].set_yscale('log')
            ax[0][0].hist(population[proto]["metrics"]["flowrate"]["data"], color = colors[0],  bins = num_bins)
            #
            # 1st col, 2nd row...
            #
            ax[0][1].set_title("Duration (secs)", fontsize = pane_title)
            ax[0][1].set_yscale('log')
            ax[0][1].hist(population[proto]["metrics"]["duration"]["data"], color = colors[1], bins = num_bins)
            ax[0][1].set_xlabel("Bin", fontsize = pane_text)
            ax[0][1].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 1st col, 3rd row...
            #
            ax[0][2].set_title("Volume (bytes)", fontsize = pane_title)
            ax[0][2].set_yscale('log')
            ax[0][2].hist(population[proto]["metrics"]["volume"]["data"], color = colors[2], bins = num_bins)
            ax[0][2].set_xlabel("Bin", fontsize = pane_text)
            ax[0][2].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 2nd col, 1st row...
            #
            ax[1][0].set_title("Average Packet Size (bytes)", fontsize = pane_title)
            ax[1][0].set_xlabel("Bin", fontsize = pane_text)
            ax[1][0].set_ylabel("log10(Counts)", fontsize = pane_text)
            ax[1][0].set_yscale('log')
            ax[1][0].hist(population[proto]["metrics"]["avpktsz"]["data"], color = colors[3],  bins = num_bins)
            #
            # 2nd col, 2nd row...
            #
            ax[1][1].set_title("Down Up Ratio", fontsize = pane_title)
            ax[1][1].set_yscale('log')
            ax[1][1].hist(population[proto]["metrics"]["dnuprat"]["data"], color = colors[4], bins = num_bins)
            ax[1][1].set_xlabel("Bin", fontsize = pane_text)
            ax[1][1].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 2nd col, 3rd row...
            #
            ax[1][2].set_title("Packet Length Variance", fontsize = pane_title)
            ax[1][2].set_yscale('log')
            ax[1][2].hist(population[proto]["metrics"]["pktlenvar"]["data"], color = colors[5], bins = num_bins)
            ax[1][2].set_xlabel("Bin", fontsize = pane_text)
            ax[1][2].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 3rd col, 1st row...
            #
            ax[2][0].set_title("Forward Packet Length Mean (bytes)", fontsize = pane_title)
            ax[2][0].set_xlabel("Bin", fontsize = pane_text)
            ax[2][0].set_ylabel("log10(Counts)", fontsize = pane_text)
            ax[2][0].set_yscale('log')
            ax[2][0].hist(population[proto]["metrics"]["fwdpktlen"]["data"], color = colors[6],  bins = num_bins)
            #
            # 3rd col, 2nd row...
            #
            ax[2][1].set_title("Backward Packet Length Mean (bytes)", fontsize = pane_title)
            ax[2][1].set_yscale('log')
            ax[2][1].hist(population[proto]["metrics"]["bwdpktlen"]["data"], color = colors[7], bins = num_bins)
            ax[2][1].set_xlabel("Bin", fontsize = pane_text)
            ax[2][1].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 3rd col, 3rd row...
            #
            ax[2][2].set_title("Active Mean", fontsize = pane_title)
            ax[2][2].set_yscale('log')
            ax[2][2].hist(population[proto]["metrics"]["actmean"]["data"], color = colors[8], bins = num_bins)
            ax[2][2].set_xlabel("Bin", fontsize = pane_text)
            ax[2][2].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # save/display or whatever...
            #
            plt.savefig(os.path.join(places("images"), f"{proto}_histogram.png"))
            if (show_histograms):
                plt.show()
            else:
                plt.close()

    print("...radar plots")
    display_proto_radar(population,
                        display_graphics = display_graphics,
                        min_count = min_count,
                        pseudo_sigmae = pseudo_sigmae,
                        anomaly_strategy = anomaly_strategy,
                        alpha_scaling = alpha_scaling)
    print("...done")
