#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-14 13:42:51 wcobb>
 
"""
#
# standard imports
#
import gzip, os, time
import math
from math import log10
import pandas as pd
import numpy as np
from scipy.stats import mode
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rc
import geopandas as gpd
from tqdm import tqdm
import dill
import seaborn as sns

import threat
from threat.core import AnomalyDetector
from threat.core import display_anomaly_statistics

if (__name__ == "__main__"):
    """
    """
    print("\nfunctional test for AnomalyDetector")
    computed = True
    if (computed):
        anomaly = AnomalyDetector(verbose = True)
        numbers = display_anomaly_statistics(anomaly.metrics)
    else:
        numbers = (10, 128, 1344, 13513, 1486164, 1, 71, 527, 0)
        
    (nr, ny, ng, nb, ni, no, nl, nt, nm) = numbers

    rc('text', usetex = True)
    internal_title  = 'Internal (Protocol Behavior) Anomalies'
    internal_colors = ["indigo", "blue", "green", "yellow", "red"]
    internal_values = [ni, nb, ng, ny, nr]
    internal_bins   = [10, 20, 30, 40, 50]
    internal_labels = ['Common', '$<$ 1/100', '$<$ 1/1K', '$<$ 1/10K', '$<$ 1/100K']
    
    external_title  = 'External (Protocol Presence) Anomalies'
    external_colors = ["violet", "magenta", "teal", "lightgreen", "orange"]
    external_values = [0, nm, nt, nl, no]
    external_bins   = [10, 20, 30, 40, 50]
    external_labels = ['$<$ 1/100', '$<$ 1/1K', '$<$ 1/10K', '$<$ 1/100K', '$<$ 1/1M']

    #
    # all the goodies...
    #
    super_size = 28
    title_size = 22
    label_size = 18
    axis_size  = 16
    fig,ax = plt.subplots(1, 2, figsize=(24, 12), facecolor='w')
    plt.suptitle("Anomaly Types And Likelihood Distribution", fontsize = super_size)
    ax[0].set_title("$\it{Behavior}$ (Unexpected Activity Pattern for Protocol)",
                    fontsize = title_size)
    ax[0].set_xlabel("Likelihood", fontsize = label_size)
    ax[0].set_ylabel("Occurrences", fontsize = label_size)
    ax[0].set_xticks(internal_bins, internal_labels, fontsize = axis_size)
    ax[0].set_yticks([0.3, 1, 3, 10, 30, 100, 300, 1000, 3000, 10000,
                      30000, 100000, 300000, 1000000, 3000000], fontsize = axis_size)
    ax[0].set_ylim((0.3, 3000000))
    ax[0].bar(internal_bins,
              internal_values,
              color = internal_colors,
              width = 10, log = True)
    ax[1].set_title("$\it{Presence}$ (Rare or Unexpected Protocol Observed)",
                    fontsize = title_size)
    ax[1].set_xlabel("Likelihood", fontsize = label_size)
    ax[1].set_ylabel("Occurrences", fontsize = label_size)
    ax[1].set_xticks(external_bins, external_labels, fontsize = axis_size)
    ax[1].set_yticks([0.3, 1, 3, 10, 30, 100, 300, 1000, 3000, 10000,
                      30000, 100000, 300000, 1000000, 3000000], fontsize = axis_size)
    ax[1].set_ylim((0.3, 3000000))
    ax[1].bar(external_bins,
              external_values,
              color = external_colors,
              width = 10, log = True)
    plt.show()




    
