#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-13 15:20:54 wcobb>
 
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
from threat.core import places

def enrich_anomaly_metrics(enriched_metrics_name = "enriched_population_metrics.dill.gz",
                           updated_metrics_name  = "updated_population_metrics.dill.gz",
                           internal_threshold:int = 1000,
                           external_threshold:int = 100,
                           overwrite = False
                           verbose = True,
                           debug = False,
                          ):
    """Enrich existing anomaly metrics by adding several new metrics
    namely 'mean_anomaly', 'max_anomaly', 'rareness', 'color', and
    'category'

    """
    enriched_metrics_path = os.path.join(places("datasets"), enriched_metrics_name)
    if (os.path.exists(enriched_metrics_path) and (not overwrite)):
        #
        # already done and not overwriting, so just return...
        #
        return None
    #
    # either hasn't been done yet or we're overwriting... let's see if we can
    # find the 'updated' metrics file...
    #
    updated_metrics_path = os.path.join(places("dataset"), updated_metrics_path)
    if (not os.path.exists(updated_metrics_path)):
        raise RuntimeError(f"could not find {updated_metrics_path} -- have you run 'test_allmetrics.py' yet?")
    metrics = dill.load(gzip.open(updated_metrics_path, "rb"))
    #
    # make the necessary updates...
    #
    proto_list = list(metrics.keys())
    total_count = 0
    for proto in proto_list:
        total_count += metrics[proto]['metrics']['avpktsz']['count']
    if (verbose):
        print(f"total_count: {total_count}")
    for proto in proto_list:
        count = metrics[proto]['metrics']['avpktsz']['count']
        if (verbose):
            print(f"{proto} (#{count}) enriching...")
        metric_keys = list(set(metrics[proto]['metrics'].keys()) - set({'path', 'flowrate', 'actmean'}))
        if ('anomaly_score' in list(metrics[proto]['metrics']['avpktsz'].keys())):
            metrics[proto]['metrics']['mean_anomaly'] = []
            metrics[proto]['metrics']['max_anomaly'] = []
            for i in range(0, count):
                subscores = []
                for key in metric_keys:
                    subscores.append(metrics[proto]['metrics'][key]['anomaly_score'][i])
                metrics[proto]['metrics']['mean_anomaly'].append(np.mean(subscores))
                metrics[proto]['metrics']['max_anomaly'].append(np.max(subscores))
        else:
            metrics[proto]['metrics']['mean_anomaly'] = [-1.0] * count
            metrics[proto]['metrics']['max_anomaly'] = [-1.0] * count
        #
        # now assign a likelihood metric... start by sorting in ASCENDING order
        #
        ranked_mean_anomaly = sorted(metrics[proto]['metrics']['mean_anomaly'], reverse = False)
        score_lookup = {}
        for i in range(0, count):
            score_lookup[f"{round(ranked_mean_anomaly[i], 5)}"] = i
        #
        # now add a likelihood metric..
        #
        metrics[proto]['metrics']['rareness'] = []
        metrics[proto]['metrics']['color'] = []
        metrics[proto]['metrics']['category'] = []
        for i in range(0, count):
            mean_anomaly = metrics[proto]['metrics']['mean_anomaly'][i]
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
            metrics[proto]['metrics']['rareness'].append(rareness)
            metrics[proto]['metrics']['color'].append(color)
            metrics[proto]['metrics']['category'].append(category)
        #
        # let user see something about the scores...
        #
        if (verbose):
            #print(f"\t...mean_anomaly scores [0:5] -- {metrics[proto]['metrics']['mean_anomaly'][0:5]}")
            #print(f"\t...max_anomaly scores [0:5]  -- {metrics[proto]['metrics']['max_anomaly'][0:5]}")
            print(f"\t...anomaly rareness [0:5] -- {metrics[proto]['metrics']['rareness'][0:5]}")
            print(f"\t...anomaly color [0:5]    -- {metrics[proto]['metrics']['color'][0:5]}")
            print(f"\t...anomaly category [0:5] -- {metrics[proto]['metrics']['category'][0:5]}")
    #
    # save the output...
    #
    dill.dump(metrics, gzip.open(enriched_metrics_path, "wb"))
    return None
        

if (__name__ == "__main__"):
    """
    """
    print("\nsmoke test for enrich_anomaly_metrics(...)")
    verbose = True
    internal_threshold = 1000
    external_threshold = 100
    metrics = enrich_anomaly_metrics(anomaly, verbose = verbose, internal_threshold = 1000, external_threshold = 100, verbose = True)

