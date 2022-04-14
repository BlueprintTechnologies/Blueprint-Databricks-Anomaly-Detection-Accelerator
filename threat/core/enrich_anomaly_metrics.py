#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-13 20:15:01 wcobb>
 
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
                           overwrite = False,
                           verbose = True,
                           debug = False,
                          ):
    """Enrich existing anomaly metrics by adding several new metrics
\    namely 'mean_anomaly', 'max_anomaly', 'rareness', 'color', and
    'category'

    """
    enriched_metrics_path = os.path.join(places("datasets"), enriched_metrics_name)
    if (os.path.exists(enriched_metrics_path) and (not overwrite)):
        #
        # already done and not overwriting, so just return...
        #
        if (verbose):
            print(f"{enriched_metrics_path} already exists so there is nothing to do")
        return None
    #
    # either hasn't been done yet or we're overwriting... let's see if we can
    # find the 'updated' metrics file...
    #
    updated_metrics_path = os.path.join(places("datasets"), updated_metrics_name)
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
        # create a sorted list of values for the mean anomaly (note that this will be
        # an ascending list)... so say the list has from (0, 500000) values, then the
        # 500,000th value would be the rarest thing in the list...
        #
        sorted_mean_anomaly = sorted(metrics[proto]['metrics']['mean_anomaly'], reverse = True)
        #
        # now associate the sorted score with the actual rank index... so say 3.554 is the
        # largest mean_anomaly score and 500,000 is the index.  then the score_lookup will
        # have 'score_lookup["3.55400"] = 500000' and we will use that later when we 
        # produce the 'rareness' number
        #
        score_lookup = {}
        for i in range(0, count):
            score_lookup[f"{round(sorted_mean_anomaly[i], 5)}"] = i
        #
        # now we'll be adding some additional content to the 'metrics' dictionary...
        #
        metrics[proto]['metrics']['rareness'] = []
        metrics[proto]['metrics']['color']    = []
        metrics[proto]['metrics']['category'] = []
        metrics[proto]['metrics']['label']    = []
        for i in range(0, count):
            #
            # read the mean anomaly value...
            #
            mean_anomaly_value = metrics[proto]['metrics']['mean_anomaly'][i]
            #
            # note that mean_anomaly_value will always be >= 0 for 'internal'
            # anomalies, but note that we have explicitly set it to < 0 as a
            # flag for 'external' anomalies...
            #
            if (mean_anomaly_value >= 0):
                #print(f"mean_anomaly = {mean_anomaly_value}")
                #
                # use the score_lookup table to read off the ranked index
                # value for this score... there are some duplicates but since
                # those are "ties" it doesn't really matter...
                #
                rareness = (count + 1)/ (1 + score_lookup[f"{round(mean_anomaly_value, 5)}"])
                #print(f"rareness = {rareness}")
                if (rareness > 1):
                    dpower = log10(rareness)
                else:
                    dpower = 0
                #print(f"dpower = {dpower}")
                category = "internal"
                if (dpower >= 5):
                    color = 'red'
                    label = f'< 1 in 100,000 {category}'
                elif (dpower >= 4):
                    color = 'yellow'
                    label = f'< 1 in 10,000 {category}'
                elif (dpower >= 3):
                    color = 'green'
                    label = f'< 1 in 1,000 {category}'
                elif (dpower >= 2):
                    color = 'blue'
                    label = f'< 1 in 100 {category}'
                else:
                    color = 'indigo'
                    label = f'common {category}'
                #print(f"color = {color}")
                #print(f"label = {label}")
                #print("----------------------------")
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
                if (dpower >= 6):
                    color = 'orange'
                    label = f'< 1 in 1,000,000 {category}'
                elif (dpower >= 5):
                    color = 'lightgreen'
                    label = f'< 1 in 100,000 {category}'
                elif (dpower >= 4):
                    color = 'teal'
                    label = f'< 1 in 10,000 {category}'
                else:
                    color = 'magenta'
                    label = f'common {category}'
            #
            # update the metrics entries...
            #
            metrics[proto]['metrics']['rareness'].append(rareness)
            metrics[proto]['metrics']['color'].append(color)
            metrics[proto]['metrics']['category'].append(category)
            metrics[proto]['metrics']['label'].append(label)
        #
        # let user see something about the scores...
        #
        if (verbose):
            print(f"\t...mean_anomaly scores [0:5] -- {metrics[proto]['metrics']['mean_anomaly'][0:5]}")
            print(f"\t...max_anomaly scores [0:5]  -- {metrics[proto]['metrics']['max_anomaly'][0:5]}")
            print(f"\t...anomaly rareness [0:5]    -- {metrics[proto]['metrics']['rareness'][0:5]}")
            print(f"\t...anomaly color [0:5]       -- {metrics[proto]['metrics']['color'][0:5]}")
            print(f"\t...anomaly category [0:5]    -- {metrics[proto]['metrics']['category'][0:5]}")
            print(f"\t...anomaly label [0:5]       -- {metrics[proto]['metrics']['label'][0:5]}")
    #
    # save the output...
    #
    dill.dump(metrics, gzip.open(enriched_metrics_path, "wb"))
    return None
        

if (__name__ == "__main__"):
    """
    """
    print("\nsmoke test for enrich_anomaly_metrics(...)")
    metrics = enrich_anomaly_metrics(internal_threshold = 1000, external_threshold = 100, verbose = True, overwrite = True)
    print("Done.")
