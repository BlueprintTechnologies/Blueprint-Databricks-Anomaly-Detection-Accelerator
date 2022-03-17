#!/usr/bin/env python
"""
Created on Monday, March 14, 2022 at 16:07:38 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-17 08:57:06 wcobb>
 
"""
#
# standard imports
#
import os, sys, time, math
import logging, logzero
from logzero import setup_logger
import dill, gzip

import threat
from threat.core import places
from threat.core import public_address
from threat.core import Cache

if (__name__ == "__main__"):
    """
    Small program for building an IP cache from network traffic data.
    In this particular case we are using the 'Unicauca V2 87Atts' dataset
    from Kaggle.  This consists of 1M records of network traffic with 
    source and destination IP addresses and lots of information about the 
    traffic itself.

    """
    print("")
    #
    # load the data...
    #
    uips_data_path = os.path.join(places("datasets"), "ip_unique_list.dill")
    if (not os.path.exists(uips_data_path)):
        raise RuntimeError(f"unable to find/load {uips_path}")
    uips_data = dill.load(open(uips_data_path, "rb"))
    #
    # instantiate a cache object...  save the output every 
    #
    cache = Cache(verbose = True, debug = True, threshold = 100)
    #
    # now loop over the possible 
    #
    for uip in uips_data:
        #
        # only consider public ip addresses...
        #
        if (public_address(uip)):
            result = cache.search(uip)
            #
            # the 'free' version of the website that we're using only allows
            # 45 free searches / minute... so wait 2s between searches...
            #
            time.sleep(2)
    #
    # show trivial summary information about cache
    #
    print(f"\n{cache}")
    print("done.")
