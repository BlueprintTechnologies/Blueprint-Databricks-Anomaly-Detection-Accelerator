#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-13 14:59:00 wcobb>
 
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
import geopandas as gpd
from tqdm import tqdm
import dill

import threat
from threat.core import AnomalyDetector

def enrich_anomaly_metrics(anomaly, verbose = False):
    """Enrich existing anomaly metrics by adding 'mean_anomaly' & 'max_anomaly'
    """
    proto_list = list(anomaly.metrics.keys())
    total_count = 0
    for proto in proto_list:
        total_count += anomaly.metrics[proto]['metrics']['avpktsz']['count']
    if (verbose):
        print(f"total_count: {total_count}")
    for proto in proto_list:
        count = anomaly.metrics[proto]['metrics']['avpktsz']['count']
        if (verbose):
            print(f"{proto} (#{count}) enriching...")
        metric_keys = list(set(anomaly.metrics[proto]['metrics'].keys()) - set({'path', 'flowrate', 'actmean'}))
        if ('anomaly_score' in list(anomaly.metrics[proto]['metrics']['avpktsz'].keys())):
            anomaly.metrics[proto]['metrics']['mean_anomaly'] = []
            anomaly.metrics[proto]['metrics']['max_anomaly'] = []
            for i in range(0, count):
                subscores = []
                for key in metric_keys:
                    subscores.append(anomaly.metrics[proto]['metrics'][key]['anomaly_score'][i])
                anomaly.metrics[proto]['metrics']['mean_anomaly'].append(np.mean(subscores))
                anomaly.metrics[proto]['metrics']['max_anomaly'].append(np.max(subscores))
        else:
            anomaly.metrics[proto]['metrics']['mean_anomaly'] = [-1.0] * count
            anomaly.metrics[proto]['metrics']['max_anomaly'] = [-1.0] * count
        #
        # now assign a likelihood metric... start by sorting in ASCENDING order
        #
        ranked_mean_anomaly = sorted(anomaly.metrics[proto]['metrics']['mean_anomaly'], reverse = False)
        score_lookup = {}
        for i in range(0, count):
            score_lookup[f"{round(ranked_mean_anomaly[i], 5)}"] = i
        #
        # now add a likelihood metric..
        #
        anomaly.metrics[proto]['metrics']['rareness'] = []
        anomaly.metrics[proto]['metrics']['color'] = []
        anomaly.metrics[proto]['metrics']['category'] = []
        for i in range(0, count):
            mean_anomaly = anomaly.metrics[proto]['metrics']['mean_anomaly'][i]
            if (mean_anomaly >= 0):
                #
                # this score is based on how peculiar the particular behavior is
                # within the category of protocol (an INTERNAL anomaly)
                #
                rareness = score_lookup[f"{round(mean_anomaly, 5)}"]
                if (rareness > 1):
                    dpower = log10(rareness)
                else:
                    dpower = 0
                category = "internal"
            else:
                #
                # this score is based on how peculiar it is for the protocol to
                # appear at all (an EXTERNAL anomaly)
                #
                rareness = int(total_count / count)
                if (rareness > 1):
                    dpower = log10(rareness)
                else:
                    dpower = 0
                category = "external"
            if (dpower >= 5):
                color = 'red'
            elif (dpower >= 4):
                color = 'orange'
            elif (dpower >= 3):
                color = 'yellow'
            elif (dpower >= 2):
                    color = 'green'
            elif (dpower >= 1):
                color = 'blue'
            else:
                color = 'indigo'
            anomaly.metrics[proto]['metrics']['rareness'].append(rareness)
            anomaly.metrics[proto]['metrics']['color'].append(color)
            anomaly.metrics[proto]['metrics']['category'].append(category)
        #
        # let user see something about the scores...
        #
        if (verbose):
            #print(f"\t...mean_anomaly scores [0:5] -- {anomaly.metrics[proto]['metrics']['mean_anomaly'][0:5]}")
            #print(f"\t...max_anomaly scores [0:5]  -- {anomaly.metrics[proto]['metrics']['max_anomaly'][0:5]}")
            print(f"\t...anomaly rareness [0:5] -- {anomaly.metrics[proto]['metrics']['rareness'][0:5]}")
            print(f"\t...anomaly color [0:5]    -- {anomaly.metrics[proto]['metrics']['color'][0:5]}")
            print(f"\t...anomaly category [0:5] -- {anomaly.metrics[proto]['metrics']['category'][0:5]}")

    # return the enhanced metrics...
    return anomaly.metrics
        

if (__name__ == "__main__"):
    """
    """
    print("\nfunctional test for AnomalyDetector")
    #
    #
    #
    verbose = True
    internal_threshold = 1000
    external_threshold = 100
    #
    # fetch population data...
    #
    anomaly = AnomalyDetector(internal_threshold = internal_threshold,
                              external_threshold = external_threshold,
                              verbose = verbose,
    )

    metrics = enrich_anomaly_metrics(anomaly, verbose = verbose)
