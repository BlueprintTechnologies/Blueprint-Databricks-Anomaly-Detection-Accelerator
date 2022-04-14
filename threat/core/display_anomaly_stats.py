#!/usr/bin/env python
"""
Created on Monday, March 21, 2022 at 14:33:41 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-04-13 20:38:13 wcobb>
 
"""
#
# standard imports
#
from math import log10

def display_anomaly_statistics(metrics:{}):
    """Display a simple ascii table summarizing
    the distribution of anomalies.

    """
    nred = 0
    nyellow = 0
    ngreen = 0
    nblue = 0
    nindigo = 0
    norange = 0
    nltgreen = 0
    nteal = 0
    nmagenta = 0
    for proto in list(metrics.keys()):
        labels = metrics[proto]['metrics']['label']
        for i in range(0, len(labels)):
            if (labels[i] == "< 1 in 100,000 internal"):
                nred += 1
            elif (labels[i] == "< 1 in 10,000 internal"):
                nyellow += 1
            elif (labels[i] == "< 1 in 1,000 internal"):
                ngreen += 1
            elif (labels[i] == "< 1 in 100 internal"):
                nblue += 1
            elif (labels[i] == "common internal"):
                nindigo += 1
            elif (labels[i] == "< 1 in 1,000,000 external"):
                norange += 1
            elif (labels[i] == "< 1 in 100,000 external"):
                nltgreen += 1
            elif (labels[i] == "< 1 in 10,000 external"):
                nteal += 1
            elif (labels[i] == "common external"):
                nmagenta += 1
            else:
                print(f"unknown label = {labels[i]}")
    print("+-------------------------------------------------+----------------------------------------+")
    print("|  INTERNAL anomalies (peculiar for protocol)     |  EXTERNAL anomalies (unusual protocol) |")
    print("+---------+---------+---------+---------+---------+---------+---------+---------+----------+")
    print("|  red    |  yellow |  green  |  blue   |  indigo |  orange | ltgreen |   teal  | magenta  |")
    print("+---------+---------+---------+---------+---------+---------+---------+---------+----------+")
    print("| <1/100K |  <1/10K |   <1/1K |  <1/100 |  >1/100 |  <1/1M  | <1/100K |  <1/10K |  >1/10K  |")
    print("+---------+---------+---------+---------+---------+---------+---------+---------+----------+")
    print("|%8d |%8d |%8d |%8d |%8d |%8d |%8d |%8d | %8d |" %
          (nred, nyellow, ngreen, nblue, nindigo, norange, nltgreen, nteal, nmagenta))
    print("+---------+---------+---------+---------+---------+---------+---------+---------+----------+")
    return None
