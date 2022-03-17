#!/usr/bin/env python
"""
Created on Monday, March 14, 2022 at 16:07:38 by 'Wesley Cobb <wesley@bpcs.com>'
Copyright (C) 2022, by Blueprint Technologies. All Rights Reserved.
 
Last edited: <2022-03-17 08:51:51 wcobb>
 
"""
#
# standard imports
#
import os, sys, time, math
import logging, logzero
from logzero import setup_logger
import dill, gzip

import threat
from threat.core import Cache

if (__name__ == "__main__"):
    """
    Trivial driver program for Cache(...)

    """
    print("")
    sample = [
        "184.62.211.87", "172.58.102.166", "172.9.168.163", "77.81.142.73",
        "154.21.208.5",  "95.182.237.3", "217.138.193.171", "24.147.105.56",
        "172.58.102.166", "172.58.99.235", "156.146.39.37",  
    ]
    #
    # instantiate a cache object with a save threshold of 8 (there are 8
    # unique addresses in our toy sample...
    #
    cache = Cache(verbose = True)
    #
    # now loop over the possible 
    #
    for ipaddr in sample:
        result = cache.search(ipaddr)
    #
    # show trivial summary information about cache
    #
    print(f"\n{cache}")
    print("done.")
