#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-12 10:32:09 wcobb>
 
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
from threat.core import display_metrics

def display_metrics(population:{},
                    min_count:int = 1,
                    num_bins = 20,
                    show_histograms:bool = False,
                    show_table:bool = True):
    """
    """
    if (show_table):
        print("ProtocolName        median(F)    median(D)     median(V)     median(A)     median(R)     median(P)")
        print("----------------- ------------ ------------  ------------  ------------  ------------  ------------")
    
    for proto in population.keys():
        if ((show_table) and (population[proto]["metrics"]["flowrate"]["count"] >= min_count)):
            print("%17s %12d %12d %12d %12d %12d %12d" % 
                  ((proto+"                 ")[0:17],
                   population[proto]["metrics"]["flowrate"]["median"],
                   population[proto]["metrics"]["duration"]["median"],
                   population[proto]["metrics"]["volume"]["median"],
                   population[proto]["metrics"]["avpktsz"]["median"],
                   population[proto]["metrics"]["dnuprat"]["median"],
                   population[proto]["metrics"]["pktlenvar"]["median"],
                  )
            )
        #
        # we're going to make 1 figure for each quantity for which we have at least
        # 1000 observations...
        #
        main_title = 24
        pane_title = 18
        pane_text = 16
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
            ax[0][0].hist(population[proto]["metrics"]["flowrate"]["data"], color = "blue",  bins = num_bins)
            #
            # 1st col, 2nd row...
            #
            ax[0][1].set_title("Duration (secs)", fontsize = pane_title)
            ax[0][1].set_yscale('log')
            ax[0][1].hist(population[proto]["metrics"]["duration"]["data"], color = "red", bins = num_bins)
            ax[0][1].set_xlabel("Bin", fontsize = pane_text)
            ax[0][1].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 1st col, 3rd row...
            #
            ax[0][2].set_title("Volume (bytes)", fontsize = pane_title)
            ax[0][2].set_yscale('log')
            ax[0][2].hist(population[proto]["metrics"]["volume"]["data"], color = "green", bins = num_bins)
            ax[0][2].set_xlabel("Bin", fontsize = pane_text)
            ax[0][2].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 2nd col, 1st row...
            #
            ax[1][0].set_title("Average Packet Size (bytes)", fontsize = pane_title)
            ax[1][0].set_xlabel("Bin", fontsize = pane_text)
            ax[1][0].set_ylabel("log10(Counts)", fontsize = pane_text)
            ax[1][0].set_yscale('log')
            ax[1][0].hist(population[proto]["metrics"]["avpktsz"]["data"], color = "magenta",  bins = num_bins)
            #
            # 2nd col, 2nd row...
            #
            ax[1][1].set_title("Down Up Ratio", fontsize = pane_title)
            ax[1][1].set_yscale('log')
            ax[1][1].hist(population[proto]["metrics"]["dnuprat"]["data"], color = "cyan", bins = num_bins)
            ax[1][1].set_xlabel("Bin", fontsize = pane_text)
            ax[1][1].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 2nd col, 3rd row...
            #
            ax[1][2].set_title("Packet Length Variance", fontsize = pane_title)
            ax[1][2].set_yscale('log')
            ax[1][2].hist(population[proto]["metrics"]["pktlenvar"]["data"], color = "brown", bins = num_bins)
            ax[1][2].set_xlabel("Bin", fontsize = pane_text)
            ax[1][2].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 3rd col, 1st row...
            #
            ax[2][0].set_title("Forward Packet Length Mean (bytes)", fontsize = pane_title)
            ax[2][0].set_xlabel("Bin", fontsize = pane_text)
            ax[2][0].set_ylabel("log10(Counts)", fontsize = pane_text)
            ax[2][0].set_yscale('log')
            ax[2][0].hist(population[proto]["metrics"]["fwdpktlen"]["data"], color = "orange",  bins = num_bins)
            #
            # 3rd col, 2nd row...
            #
            ax[2][1].set_title("Backward Packet Length Mean (bytes)", fontsize = pane_title)
            ax[2][1].set_yscale('log')
            ax[2][1].hist(population[proto]["metrics"]["bwdpktlen"]["data"], color = "lightgreen", bins = num_bins)
            ax[2][1].set_xlabel("Bin", fontsize = pane_text)
            ax[2][1].set_ylabel("log10(Counts)", fontsize = pane_text)
            #
            # 3rd col, 3rd row...
            #
            ax[2][2].set_title("Active Mean", fontsize = pane_title)
            ax[2][2].set_yscale('log')
            ax[2][2].hist(population[proto]["metrics"]["actmean"]["data"], color = "indigo", bins = num_bins)
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
    return None
